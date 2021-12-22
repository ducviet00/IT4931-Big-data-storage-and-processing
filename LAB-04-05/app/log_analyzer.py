from pyspark import SparkContext
from pyspark.streaming import StreamingContext, Seconds
import re
from typing import NamedTuple


class ApacheAccessLog(NamedTuple):
    ipAddress: str 
    clientIdentd: str
    userId: str
    dateTime: str
    method: str
    endpoint: str
    protocol: str
    responseCode: int
    contentSize: int

def parseLogLine(log):
    pattern = r"""^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+)"""
    res = re.findall(pattern, log)[0]
    return ApacheAccessLog(*res)

def analyze(accessLogs):
    if accessLogs.count() == 0:
        println("No access logs received in this time interval")
    else:
        contentSizes = accessLogs.map(_.contentSize).cache()
        print(f"Content Size Avg: {contentSizes.reduce(_ + _) / contentSizes.count,}, \
                Min: {contentSizes.min}, \
                Max: {contentSizes.max}")
        responseCodeToCount = accessLogs.map(int(_.responseCode)).reduceByKey(_ + _).take(100)
        println(f'Response code counts: {responseCodeToCount}')
        ipAddresses = accessLogs.map(_.ipAddress).reduceByKey(_ + _).filter(_._2 > 10).map(_._1).take(100)
# Create a local StreamingContext with two working thread and batch interval of 10 second
sc = SparkContext(appName="Log Analyzer Streaming in Scala")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 10)
logLinesDStream = ssc.socketTextStream("lab-04-05_spark_1", 9999)
logLinesDStream = logLinesDStream.filter(lambda line: not line.endswith("-"))
accessLogsDStream = logLinesDStream.map(parseLogLine).cache()
windowDStream = accessLogsDStream.window(30, 10)


windowDStream.foreachRDD(func)

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
