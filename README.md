# Building a Big Data architecture in the cloud (Workshop)

Repository for a workshop to build an architecture in cloud with AWS EMR and Spark.

We will create and architecture to obtain and process some events or records in a Big Data environment in cloud (AWS  in this case).

Requirements: 

Amazon AWS account: https://aws.amazon.com/

Python 3.6 or higher:  https://www.python.org/downloads/release/python-360/ or https://www.anaconda.com/

Spark 2.4.5 or higher: https://spark.apache.org/docs/2.4.5/

Putty or other SSH connector: https://www.putty.org/

SFTP connector program such as Cyberduck: https://cyberduck.io/

Steps.

1. **Understanding the problem:**

   A company works with event monitoring devices that detect certain signals such as gas leaks or signals from a vehicle or any IoT signal or positions of an employee or an object or they can also be confirmations of activities that have been done.
   This process is carried out in real time but it can also have an alternative process in which it receives all the events in batch to be processed and after being classified, they can be stored together with the events that arrive in real time. The final result can be to be viewed in a web application.

   An example of the complete process is drawn below:

![Process](images\Process.PNG)



2. **Process:**

   a. Analyze the functionalities.

   b. Analyze the quality attributes, for example in this case: Is very important to follow a stream process with low latency, good reliability and availability. However, other attributes like usability or interoperability maybe can be good drivers of our architecture. 

   (To understand this attributes and the process to create the drivers you can read: [Software Architecture & Quality Attributes](https://sites.google.com/site/misresearch000/home/software-architecture-quality-attributes#:~:text=There%20are%20three%20main%20categories,%2C%20testability%2C%20usability%2C%20others.&text=Architectural%20Qualities%3A%20conceptual%20integrity%2C%20correctness%20and%20completeness.))

   c. Write the non-functionalities requirements. 

   d.  Determinate the  enterprise environment, for example the components in your company are on-premise or there are in a private cloud or in a different cloud that you know. It is important to analyze cost, efforts and the disposition to make any change. 

   e. Fit the "LEGO pieces"

3. Propose of draw of architecture: (This is just one of the many approaches)

   ![Architecture](images\Demo architecture.PNG)

