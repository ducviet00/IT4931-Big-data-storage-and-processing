name := "logs-analyzer" 
version := "0.0.1"
scalaVersion := "2.12.15" // additional libraries
libraryDependencies ++= Seq(
"org.apache.spark" %% "spark-core" % "3.2.0" % "provided", 
"org.apache.spark" %% "spark-streaming" % "3.2.0"
)