FROM cm2network/steamcmd:root

# Install Python and watchdog dependencies
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Create a virtual environment for Python packages
RUN python3 -m venv /opt/venv

# Activate the virtual environment and install watchdog
RUN /opt/venv/bin/pip install watchdog pygrok

# Define environment variables
ENV STEAMAPPID=343050
ENV STEAMAPP=dst
ENV STEAMAPPDIR="${HOMEDIR}/${STEAMAPP}-dedicated"

# Set HOME to /home/steam to fix the permission issue
ENV HOME=/home/steam

# Install dependencies for 32-bit libraries and TMUX for server management
RUN set -x && \
    dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y libcurl4-gnutls-dev:i386 tmux vim less && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Don't Starve Together using SteamCMD in the Docker build
RUN bash "${STEAMCMDDIR}/steamcmd.sh" \
    +force_install_dir "${STEAMAPPDIR}" \
    +login anonymous \
    +app_update "${STEAMAPPID}" validate \
    +quit

# Copy the entrypoint script into the container and set ownership to steam user
COPY --chown=steam:steam entry.sh "${HOMEDIR}/entry.sh"
RUN chmod +x "${HOMEDIR}/entry.sh"

# Copy the log monitor script into the container and set ownership to steam user
COPY --chown=steam:steam log_monitor.py "${HOMEDIR}/log_monitor.py"
RUN chmod +x "${HOMEDIR}/log_monitor.py"

# Copy the common directory into the container
COPY --chown=steam:steam common/ "${HOMEDIR}/common/"

# Copy the handlers directory into the container
COPY --chown=steam:steam handlers/ "${HOMEDIR}/handlers/"

# Create directory for the DST dedicated server files and change ownership and permissions
RUN mkdir -p "${STEAMAPPDIR}" && \
    chown -R steam:steam "${STEAMAPPDIR}" && \
    chmod -R 755 "${STEAMAPPDIR}"

# Switch to the non-root user 'steam'
USER steam

# Set the working directory to the home directory of the steam user
WORKDIR ${HOMEDIR}

# Create folder for server settings and ensure ownership/permissions
RUN mkdir -p "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Master" \
             "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Caves"

# Copy Overworld (Master) shard configuration with ownership set to steam
COPY --chown=steam:steam "config/Cluster_1/Overworld/server.ini" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Master/server.ini"
COPY --chown=steam:steam "config/Cluster_1/Overworld/worldgenoverride.lua" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Master/worldgenoverride.lua"
COPY --chown=steam:steam "config/Cluster_1/Overworld/leveldataoverride.lua" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Master/leveldataoverride.lua"

# Copy Caves shard configuration with ownership set to steam
COPY --chown=steam:steam "config/Cluster_1/Caves/server.ini" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Caves/server.ini"
COPY --chown=steam:steam "config/Cluster_1/Caves/worldgenoverride.lua" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Caves/worldgenoverride.lua"

# Copy shared configuration files (adminlist, blocklist, etc.) with ownership set to steam
COPY --chown=steam:steam "config/Cluster_1/adminlist.txt" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/adminlist.txt"
COPY --chown=steam:steam "config/Cluster_1/blocklist.txt" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/blocklist.txt"
COPY --chown=steam:steam "config/Cluster_1/whitelist.txt" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/whitelist.txt"

# Copy the cluster.ini file with ownership set to steam
COPY --chown=steam:steam "config/Cluster_1/cluster.ini" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/cluster.ini"

# Copy mod files
COPY --chown=steam:steam "config/mods/dedicated_server_mods_setup.lua" "${STEAMAPPDIR}/mods/dedicated_server_mods_setup.lua"
COPY --chown=steam:steam "config/mods/modsettings.lua" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Master/modoverrides.lua"
COPY --chown=steam:steam "config/mods/modsettings.lua" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Caves/modoverrides.lua"

# Set the entry point to run the entry.sh script and the Python log monitor script
ENTRYPOINT ["bash", "-c", "./entry.sh & /opt/venv/bin/python3 ./log_monitor.py"]

# Expose necessary ports
EXPOSE 11000/udp
EXPOSE 11003/udp
