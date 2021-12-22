from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Create a local StreamingContext with two working thread and batch interval of 10 second
sc = SparkContext(appName="Socket-Stream-Python")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 10)
logLinesDStream = ssc.socketTextStream("lab-04-05_spark_1", 7777)
accessLogsDStream = logLinesDStream.map(ApacheAccessLog.parseLogLine).cache()
# Filter our DStream ​for​ lines with ​"error"
# error_lines = lines.filter(lambda line: "error" in line)
# error_lines.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
