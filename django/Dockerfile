FROM scratch
ADD ubuntu-xenial-core-cloudimg-amd64-root.tar.gz /
ADD /usr /usr
ADD /virtualenv /root/virtualenv
RUN apt-get install python vim -y
CMD ["/bin/bash"]
