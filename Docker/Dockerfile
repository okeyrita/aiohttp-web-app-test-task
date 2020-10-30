FROM fedora:32


RUN curl -s https://repos.fedorapeople.org/repos/thl/kernel-vanilla.repo
RUN sudo tee /etc/yum.repos.d/kernel-vanilla.repo

#RUN sudo dnf -y update && dnf clean all
#RUN sudo dnf upgrade
RUN sudo dnf --enablerepo=kernel-vanilla-stable update

RUN sudo dnf config-manager --set-enabled kernel-vanilla-stable