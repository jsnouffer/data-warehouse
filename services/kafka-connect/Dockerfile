FROM kubeless/unzip:latest as builder

RUN curl --remote-name --location --silent https://d1i4a15mxbxib1.cloudfront.net/api/plugins/confluentinc/kafka-connect-jdbc/versions/10.2.3/confluentinc-kafka-connect-jdbc-10.2.3.zip && \
    unzip confluentinc-kafka-connect-jdbc-10.2.3.zip

RUN curl --remote-name --location --silent https://repo1.maven.org/maven2/org/mariadb/jdbc/mariadb-java-client/3.0.2-rc/mariadb-java-client-3.0.2-rc.jar
RUN curl --remote-name --location --silent https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.26/mysql-connector-java-8.0.26.jar

# FROM bitnami/kafka:2
FROM confluentinc/cp-kafka-connect:latest

COPY --from=builder /confluentinc-kafka-connect-jdbc-10.2.3/lib/* /usr/share/java/kafka-connect-jdbc/
# COPY --from=builder /confluentinc-kafka-connect-jdbc-10.2.3/etc/* /opt/bitnami/kafka/config/
COPY --from=builder /mariadb-java-client*.jar /usr/share/java/kafka-connect-jdbc/
COPY --from=builder /mysql-connector-java*.jar /usr/share/java/kafka-connect-jdbc/

# CMD /opt/bitnami/kafka/bin/connect-standalone.sh /opt/bitnami/kafka/config/connect-standalone.properties /opt/bitnami/kafka/config/sink-quickstart-sqlite.properties
