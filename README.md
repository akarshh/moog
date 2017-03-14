# moog
Machine Health Monitoring System
for the Mazak VCU400-5X machine

Pre-requisites:

1. Python 3.5
2. An InitialState account
3. Acccelerometer sensor, Fluid Level sensor, Temperature sensor all connected to an Arduino and a Raspberry Pi or computer

To begin logging data onto the InitialState platform follow these steps:

1. Create a unique API key on InitialState for each machine. This is what will be used to POST data to the server via HTTPS.
2. Run the following commands on the terminal. These will install all required python libraries:
        1. pip3 install ISStreamer
        2. pip3 install pyserial
3. Use the following format to POST data:
        from ISStreamer.Streamer import Streamer
        streamer = Streamer(bucket_name="MoogTest", bucket_key="5LRM9UG8CASH",
                    access_key="NCbUQzFnRPMVoXDSjUL40Paxs0ICSV0Q")
        streamer.log("Key", value)
       
