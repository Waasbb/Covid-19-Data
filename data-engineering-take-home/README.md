# Data-Engineering-Take-Home Solution #

## How to run app once LocalStack has started

1. Navigate to the project root directory

2. Execute the python script with `python queue_app.py`

 

## Thought Process...

My solution for this process was to use boto3 -- an aws library which allows using to interact with AWS services -- in this case SQS. I needed a way to read messages from the queue which could be done using the SQS function `revieve_message()`. This would allow me to define what kind of polling I need -- whether short or long. In this case, I decided with short.

From there, I also needed to figure out how to mask the device_id and ip values. I decided to go with a `hash masking` approach. This would allow me to have the same hash for values that are duplicates.

The application currently runs via a script, however, if this was done in AWS I could go with a serverless approach using `Lambda` where it would listen for SQS events and execute the script.


