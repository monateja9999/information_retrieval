FULL NAME: MONA TEJA KURAKULA

Dear Grader/CP/TA/Prof. Saty,

I have completed the assignment locally by installing Apache Hadoop on my laptop. 

Hadoop Version Used: 3.3.6
Java JDK Version Used: java version "1.8.0_202"

INSTALLATION AND CONFIGURATION SETUP:

STEP 1: I have referred the following video for majority of my configuration and setup of Hadoop locally on my computer.

LINK: https://www.youtube.com/watch?v=knAS0w-jiUk

STEP 2: You can choose to use local mode in mapred-site.xml if you don't want to use Yarn and without dependency on internet. Ref below as follows (optional: only if you want to run the map-reduce locally) 

<configuration>
   <property>
      <name>mapreduce.framework.name</name>
      <value>local</value>
   </property>
</configuration>

STEP 3: I have used hadoop streaming jar as it allows the user to write custom mappers in different languages other than Java.

STEP 4: My Implementation is in python and you can find the source codes in src folder. I have unigram_mapper.py, bigram_mapper.py and have a common reducer for both tasks named unigram_reducer.py


STEPS OF EXECUTION:

1. Open CMD in Administrator mode, ensure that hadoop is installed as per the video provided above.

2. Now use start-all.cmd to start namenode, datanode, nodemanager and resourcemanager are running using jps command. Then for the first time use hdfs namenode -format to setup the initial structure for the project.

3. Firstly, we need to load the devdata and fulldata into hadoop filesystem using hdfs dfs -put <localpath of data> <hdfs source (Ex: /input)>

4. Then we can perform mapreduce using the following example command (paths might be local to your placement of the files)


FOR UNIGRAMS:

hadoop jar C:\hadoop\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar -input /input/fulldata -output /output/unigram_index -mapper "python C:/Users/monat/Desktop/IR_HW_3/src/unigram_mapper.py" -reducer "python C:/Users/monat/Desktop/IR_HW_3/src/unigram_reducer.py" -file C:/Users/monat/Desktop/IR_HW_3/src/unigram_mapper.py -file C:/Users/monat/Desktop/IR_HW_3/src/unigram_reducer.py


FOR BIGRAMS:

hadoop jar C:\hadoop\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar -input /input/devdata -output /output/bigram_index -mapper "python C:/Users/monat/Desktop/IR_HW_3/src/bigram_mapper.py" -reducer "python C:/Users/monat/Desktop/IR_HW_3/src/unigram_reducer.py" -file C:/Users/monat/Desktop/IR_HW_3/src/bigram_mapper.py -file C:/Users/monat/Desktop/IR_HW_3/src/unigram_reducer.py

(if output folder already exists i.e., it is not being executed for the first time, to ensure the command is successfully executed use the following command)

hdfs dfs -rm -r /output

5. Now the output will be generated in the hadoop filesystem. In order for the user to see the output and want it in a txt file we need to use the -get command to retrieve the output to required txt format as expected for the assignment.

FOR UNIGRAMS:

hdfs dfs -get /output/unigram_index C:\Users\monat\Desktop\IR_HW_3\output\unigram_index


FOR BIGRAMS:

hdfs dfs -get /output/bigram_index C:\Users\monat\Desktop\IR_HW_3\output\selected_bigram_index


6. In the output folders, we can see a SUCESS FILE and part-00000 file by default. Now rename this part-00000 to unigram_index.txt or selected_bigram_index.txt as per the folder and this can be viewed using any text editor to verify the results.


THANK YOU!!!
