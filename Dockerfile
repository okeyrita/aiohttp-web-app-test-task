FROM fedora:32

# Install vanilla kernel
RUN curl -s https://repos.fedorapeople.org/repos/thl/kernel-vanilla.repo | sudo tee /etc/yum.repos.d/kernel-vanilla.repo
RUN sudo dnf -y --enablerepo=kernel-vanilla-stable update
RUN sudo yum -y install dnf-plugins-core
RUN sudo dnf config-manager --set-enabled kernel-vanilla-stable

# Install python packages
RUN dnf update python3
RUN dnf -y install python3-aiohttp

# Copy project to container
RUN mkdir test_task
COPY aiohttptest_task /test_task

# Run app
EXPOSE 8080

CMD cd test_task && python3 entry.py