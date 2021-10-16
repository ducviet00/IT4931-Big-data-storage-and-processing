# Install java
sudo apt update
sudo apt install default-jdk
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz
tar -xzvf hadoop-3.3.1.tar.gz
sudo mv hadoop-3.3.1 /usr/local/hadoop
echo 'export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
echo 'PATH=/usr/local/hadoop/bin:/usr/local/hadoop/sbin:$PATH' >> ~/.profile
echo 'export HADOOP_HOME=/usr/local/hadoop' >> ~/.bashrc
echo 'export PATH=${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin' >> ~/.bashrc
/usr/local/hadoop/bin/hadoop version

cd ~/IT4931-Big-data-storage-and-processing/LAB-01
cp etc/* /usr/local/hadoop/etc/hadoop/
