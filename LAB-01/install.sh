# Install java
sudo apt update
sudo apt install default-jdk -y
sudo cp hosts /etc/
cd ~
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz
tar -xzvf hadoop-3.3.1.tar.gz
sudo mv hadoop-3.3.1 /usr/local/hadoop
echo 'export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
echo 'export HDFS_NAMENODE_USER="root"' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
echo 'export HDFS_DATANODE_USER="root"' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
echo 'export HDFS_SECONDARYNAMENODE_USER="root"' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
echo 'export YARN_RESOURCEMANAGER_USER="root"' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
echo 'export YARN_NODEMANAGER_USER="root"' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
source /usr/local/hadoop/etc/hadoop/hadoop-env.sh
echo 'PATH=/usr/local/hadoop/bin:/usr/local/hadoop/sbin:$PATH' >> ~/.profile
echo 'export HADOOP_HOME=/usr/local/hadoop' >> ~/.bashrc
echo 'export PATH=${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin' >> ~/.bashrc
echo 'HADOOP VERSION'
/usr/local/hadoop/bin/hadoop version

cd ~/IT4931-Big-data-storage-and-processing/LAB-01
cp etc/* /usr/local/hadoop/etc/hadoop/
