Title: IMPBus2 Implementation QuickStart Manual
Date: 2013-06-26
Category: development
Tags: impbus2, imko, sensor
Slug: impbus2-implementation
Author: Markus Hubig
Summary: QuickStart manual covering the basics of implementing the minimal
         set of commands needed to talk to IMPBus2 enabled devices.
status: draft

This document should be a practical quick-start introduction to the IMPBus2
Protocol by IMKO GmbH and serves as a practical guideline to implement the
simple commands that are needed to utilize a IMKO GmbH Pico sensor to start a
measurement and get the resulting data back.

Before diving into more details, let's do a quick summary about how the minimal
needed communication loop would look like (Pseudocode!).

     # After powering on the probes.
     for each sensor in list_of_sensors:
         start_measurement(sensor)
         while measurement_running(sensor):
             time.sleep(0.500)
         get_measurement_data(sensor)

So there are effectively just three commands to implement:

    1. start_measurement()
    2. measurement_is_running()
    3. get_measurement_data()

> **NOTE**  
> We are developing a reference implementation of the IMPBus2 protocol. The
> resulting library is Open Source (LGPL) so you can easily include this
> library into your own application. But since it is written in Python you may
> need to port things over to cover you needs. You can find more infomation and
> the actual code here:
>
> <http://implib2.imko.de>  
> <https://bitbucket.org/imko/implib2>
>
> This HowTo will include snippets from the implib2 python library and in order
> to make it easy for everyone to reproduce the data frames with the correct
> CRC checksum. It is highly recommended to install
> [implib2](https://bitbucket.org/imko/implib2), startup a
> [ipython](http://ipython.org/) shell and prepare the following testing
> environment:
>
>     In [1]: from binascii import a2b_hex as a2b, b2a_hex as b2a
>     In [2]: from implib2 import Bus, Module
>     In [3]: bus = Bus('loop://')
>
> Now it is possible to easily construct IMPBus2 data frames or compute CRC
> checksum with commands like this:
>
>     In [4]: b2a(bus.cmd.get_parameter(324456,
>       ....: 'MEASURE_PARAMETER_TABLE',
>       ....: 'Moist'))
>     Out[4]: 'fd160368f3047d0a00e7'
>     In [5]: b2a(bus.cmd.pkg.crc.calc_crc(a2b('00168168F304')))
>     Out[5]: '9b'

## <a id="info"></a> General info

IMPBus2 is a bus system to which up to 60 single slaves may be connected by a
bi-directional 2-wire line. The IMPBus2 utilize a single master serial bus
protocol. All commands are invoked by the bus master and adressed to one or
more probes. The communication is based on the transmission of address- and
data blocks. Up to 250 bytes of significant data can be transmitted
bi-directional in one telegram.

#### <a id="addressblock"></a> IMPBus2 Adressblock:

    <FD> <CMD> <Length> <Address> <CRC>
     |    |     |        |         |
     |    |     |        |         `- Maxim/Dallas 1-Wire CRC
     |    |     |        `- Address of the target probe
     |    |     `- Length of the data block
     |    `- Command for the Probe
     `- IMP232N protocol indicator

#### <a id="datablock"></a> IMPBus2 Datablock:

    <Data> <CRC>
     |      |
     |      `- Maxim/Dallas 1-Wire CRC
     `- Up to 252 bytes

#### <a id="tables"></a> Tables:

The command structure of the IMPBus2 protocol is table-based. There are tables
such as **system parameter table** or the **action parameter table** and the
`<CMD>` field in the IMPBus2 Adressblock is used to select the particular
table, either in write or read mode. The `<Data>` field in the IMPBus2
Datablock is used to select the table **cell** and, optionally, carry the data
to write into the table cell. For more in depth information on the parameter
tables, please refer to the full [Protocol Manual](http://imko.de/protocol).

#### <a id="address"></a> Address a probe:

The IMPBus2 address space consists of 4-bytes (0-16.777.215 or 0x00-0xffffff).
To address a probe, the serial number of the probe has to be converted into a
`little-endian unsigned int` with the most-significant bytes cut off.

    Y  serial number: 324456
    |  hex: [00] 04 f3 68 (Big-Endian)
    |  bin: [0000-0000] 0000-0100 1111-0011 0110-1000 (Big-Endian)
    |  bin: 0110-1000 1111-0011 0000-0100 [0000-0000] (Little-Endian)
    |  hex: 68 f3 04 [00] (Little-Endian)
    V  probe address: 68f304

#### <a id="serial"></a> Setup the serial interface

Set your serial interface to the following RS-232C/V24 data format:

    1 start bit
    8 data bits
    1 parity bit (odd parity)
    2 stop bits

You can use the following standard baud rates: `1200`, `2400`, `4800` or
`9600`.

#### <a id="crc"></a> Calculation of the CRC's

The IMPBus2 Protocol uses the Maxim 1-Wire CRC algorythm to secure the data
transmission. You can use the following (python) code snipped as reference on
how to calculate the CRC's. For more information rever to the Maxim/Dallas
manual [DS18B20](http://datasheets.maximintegrated.com/en/ds/DS18B20.pdf)

    tbl = [ 0,  94, 188, 226,  97,  63, 221, 131, 194, 156, 126,
           32, 163, 253,  31,  65, 157, 195,  33, 127, 252, 162,
           64,  30,  95,   1, 227, 189,  62,  96, 130, 220,  35,
          125, 159, 193,  66,  28, 254, 160, 225, 191,  93,   3,
          128, 222,  60,  98, 190, 224,   2,  92, 223, 129,  99,
           61, 124,  34, 192, 158,  29,  67, 161, 255,  70,  24,
          250, 164,  39, 121, 155, 197, 132, 218,  56, 102, 229,
          187,  89,   7, 219, 133, 103,  57, 186, 228,   6,  88,
           25,  71, 165, 251, 120,  38, 196, 154, 101,  59, 217,
          135,   4,  90, 184, 230, 167, 249,  27,  69, 198, 152,
          122,  36, 248, 166,  68,  26, 153, 199,  37, 123,  58,
          100, 134, 216,  91,   5, 231, 185, 140, 210,  48, 110,
          237, 179,  81,  15,  78,  16, 242, 172,  47, 113, 147,
          205,  17,  79, 173, 243, 112,  46, 204, 146, 211, 141,
          111,  49, 178, 236,  14,  80, 175, 241,  19,  77, 206,
          144, 114,  44, 109,  51, 209, 143,  12,  82, 176, 238,
           50, 108, 142, 208,  83,  13, 239, 177, 240, 174,  76,
           18, 145, 207,  45, 115, 202, 148, 118,  40, 171, 245,
           23,  73,   8,  86, 180, 234, 105,  55, 213, 139,  87,
            9, 235, 181,  54, 104, 138, 212, 149, 203,  41, 119,
          244, 170,  72,  22, 233, 183,  85,  11, 136, 214,  52,
          106,  43, 117, 151, 201,  74,  20, 246, 168, 116,  42,
          200, 150,  21,  75, 169, 247, 182, 232,  10,  84, 215,
          137, 107, 53]

    def crc(byte_str):
        register = 0x00
        for char in byte_str:
            tbl_idx = (register ^ ord(char)) & 0xff
            register = ((register >> 0x08) ^ tbl[tbl_idx]) & 0xff
        return chr(register) # unsigned char

## <a id="measurement"></a> HowTo start a measurement and get the data.

In this example we assume that we have a single Pico probe connected to our
Master(Computer) via the RS232 serial interface port and a RS232-to-IMPBus
converter, like the SM23U or the SM-USB. The Pico probe has the serial number
`324456` and the serial interface is setup [as stated above](#serial).

00. The communication starts with the master sending the `start measurement`
    command.

        ,-------,                    ,--------,
        | pico  |-------RS232--------| Master |
        `-------´                    `--------´
            ^                             V
            |_____ Start Measurement _____|

    As mentioned above [tables], sending a command is synonym to writing
    something into a particular table cell on the probe. So in order to start
    the measurement we need to write the value `1` into the `StartMeasure` cell
    of the `Action-Parameter-Table`. The resulting data frame looks like this:

        ------header------  ---data----
        FD 15 04 68F304 B5  06 00 01 8F
        -- -- -- ------ --  -- -- -- --
        |  |  |  |      |   |  |  |  |
        |  |  |  |      |   |  |  |  `- CRC of data block
        |  |  |  |      |   |  |  `- Value to write into cell
        |  |  |  |      |   |  `- Always 0x00!
        |  |  |  |      |   `- StartMeasure-cell
        |  |  |  |      `- CRC of the first 6 Bytes
        |  |  |  `- Converted address (324456) of the probe
        |  |  `- Length of the following data block is 4 bytes
        |  `- SET action-parameter-table command
        `- IMP232N protocol indicator

        # HowTo get this data frame with the IMPLib2
        In [7]: bus.cmd.set_parameter(324456,
        ...:        'ACTION_PARAMETER_TABLE',
        ...:        'StartMeasure', [1])
        Out[7]: '\xfd\x15\x04h\xf3\x04\xb5\x06\x00\x01\x8f'

00. Now the Probe will answer with just a header block that copies the command
    from the request (SET action-parameter-table). If something goes wrong with
    the first byte of the header will be `!= 0`.

        ------header------
        00 15 00 68F304 83
        -- -- -- ------ --
        |  |  |  |      |
        |  |  |  |      `- CRC
        |  |  |  `- Converted address (324456) of the probe
        |  |  `- Length of the following data block (0 = no block)
        |  `- SET action-parameter-table command
        `- 00 Error code (00 = O.K.)

00. The measuring is now in progress. When the probe finishes the measuring,
    the value of the `Action-Parameter-Table` cell `StartMeasure` will be
    switched back to `0`. The needed data frame to request the measurement
    state can be constructed as follows:

        ------header------  --data--
        FD 14 03 68F304 FE  06 00 AA
        -- -- -- ------ --  -- -- --
        |  |  |  |      |   |  |  |
        |  |  |  |      |   |  |  `- CRC of data block
        |  |  |  |      |   |  `- Alwayse 0x00!
        |  |  |  |      |   `- StartMeasure-cell
        |  |  |  |      `- CRC of the first 6 Bytes
        |  |  |  `- Converted address (324456) of the probe
        |  |  `- Length of the following data block is 4 bytes
        |  `- GET Action-Parameter-Table command
        `- IMP232N protocol indicator

        # HowTo get this data frame with the IMPLib2
        In [8]: bus.cmd.get_parameter(324456,
        ...:             'ACTION_PARAMETER_TABLE',
        ...:             'StartMeasure')
        Out[8]: '\xfd\x14\x03h\xf3\x04\xfe\x06\x00\xaa'

    And is answered with measurement **in progress** (`Value=0x01`):

        ------header------  -data-
        00 14 02 68F304 49  01  5E
        -- -- -- ------ --  --  --
        |  |  |  |      |   |   |
        |  |  |  |      |   |   `- CRC
        |  |  |  |      |   `- Value=0x01
        |  |  |  |      `- CRC
        |  |  |  `- Converted address (324456) of the probe
        |  |  `- Length of the following data block
        |  `- GET action-parameter-table command
        `- 00 Error code (00 = O.K.)

     And with measurement **finished** (`Value=0x00`):

        ------header------  -data-
        00 14 02 68F304 49  00  00
        -- -- -- ------ --  --  --
        |  |  |  |      |   |   |
        |  |  |  |      |   |   `- CRC
        |  |  |  |      |   `- Value=0x00
        |  |  |  |      `- CRC
        |  |  |  `- Converted address (324456) of the probe
        |  |  `- Length of the following data block
        |  `- GET action-parameter-table command
        `- 00 Error code (00 = O.K.)

    So we need to start a little loop and wait for the measurement to finish.

        while measurement_running():
            time.sleep(0.500)

00. Now all what's left to do is to request the measurement data from the
    Probe. The measurement data is stored in the `Measure-Parameter-Table`.
    To get the moisture data, send the following data frame:

        ------header------  --data--
        FD 16 03 68F304 7D  0A 00 E7
        -- -- -- ------ --  -- -- --
        |  |  |  |      |   |  |  |
        |  |  |  |      |   |  |  `- CRC of data block
        |  |  |  |      |   |  `- Always 0x00!
        |  |  |  |      |   `- 0xFF means 'get all cells'
        |  |  |  |      `- CRC of the first 6 Bytes
        |  |  |  `- Converted address (324456) of the probe
        |  |  `- Length of the following data block is 3 bytes
        |  `- GET Measure-Parameter-Table command
        `- IMP232N protocol indicator

        # HowTo get this data frame with the IMPLib2
        In [9]: b2a(bus.cmd.get_parameter(324456,
        ...: 'MEASURE_PARAMETER_TABLE',
        ...: 'Moist'))
        Out[9]: 'fd160368f3047d0a00e7'

    This will be answerd from the probe with a data frame like this, containing
    the moisture value:

        ------header------  ---data----
        00 16 81 68F304 9B  EC51F441 31
        -- -- -- ------ --  -------- --
        |  |  |  |      |   |        |
        |  |  |  |      |   |        `- CRC of Data block
        |  |  |  |      |   `- Moist value 32 Bit Float (30.54 %)
        |  |  |  |      `- CRC of the first 6 Bytes
        |  |  |  `- Converted address (324456) of the probe
        |  |  `- Length of the following data block is 3 bytes
        |  `- GET Measure-Parameter-Table command
        `- IMP232N protocol indicator

    Or if you need the temperature, send this data frame:

        ------header------  --data--
        FD 16 03 68F304 7D  0D 00 89
        -- -- -- ------ --  -- -- --
        |  |  |  |      |   |  |  |
        |  |  |  |      |   |  |  `- CRC of data block
        |  |  |  |      |   |  `- Alwayse 0x00!
        |  |  |  |      |   `- 0xFF means 'get all cells'
        |  |  |  |      `- CRC of the first 6 Bytes
        |  |  |  `- Converted address (324456) of the probe
        |  |  `- Length of the following data block is 3 bytes
        |  `- GET Measure-Parameter-Table command
        `- IMP232N protocol indicator

        # HowTo get this data frame with the IMPLib2
        In [10]: b2a(bus.cmd.get_parameter(324456,
            ...: 'MEASURE_PARAMETER_TABLE',
            ...: 'CompTemp'))
        Out[25]: 'fd160368f3047d0d0089'

    This will be aswered by the probe with:

        ------header------  ---data----
        00 16 81 68F304 9B  0000ac41 BB
        -- -- -- ------ --  -------- --
        |  |  |  |      |   |        |
        |  |  |  |      |   |        `- CRC of Data block
        |  |  |  |      |   `- Moist value 32 Bit Float (21.5 °C)
        |  |  |  |      `- CRC of the first 6 Bytes
        |  |  |  `- Converted address (324456) of the probe
        |  |  `- Length of the following data block is 3 bytes
        |  `- GET Measure-Parameter-Table command
        `- IMP232N protocol indicator


00. If you have more than one sensor connected to the IMPBus2, you have to
    repeat this process for each sensor.
