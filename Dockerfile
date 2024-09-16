FROM cm2network/steamcmd:root

# Define environment variables
ENV STEAMAPPID=343050 \
    STEAMAPP=dst \
    HOME=/home/steam

ENV STEAMAPPDIR="${HOMEDIR}/${STEAMAPP}-dedicated"

# Install dependencies, set up Python environment, and install DST server in a single RUN command
RUN set -x && \
    dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        libcurl4-gnutls-dev:i386 \
        tmux \
        vim \
        less \
        procps && \
    python3 -m venv "/opt/venv" && \
    "/opt/venv/bin/pip" install watchdog pygrok && \
    apt-get clean && \
    rm -rf "/var/lib/apt/lists/*" "/tmp/*" "/var/tmp/*" && \
    bash "${STEAMCMDDIR}/steamcmd.sh" \
        +force_install_dir "${STEAMAPPDIR}" \
        +login anonymous \
        +app_update "${STEAMAPPID}" validate \
        +quit && \
    mkdir -p "${STEAMAPPDIR}" && \
    chown -R steam:steam "${STEAMAPPDIR}" && \
    chmod -R 755 "${STEAMAPPDIR}"

# Copy scripts and set permissions
COPY --chown=steam:steam "entry.sh" "log_monitor.py" "health_check.py" "${HOMEDIR}/"
RUN chmod +x "${HOMEDIR}/entry.sh" "${HOMEDIR}/log_monitor.py" "${HOMEDIR}/health_check.py"

# Copy directories
COPY --chown=steam:steam "common/" "${HOMEDIR}/common/"
COPY --chown=steam:steam "handlers/" "${HOMEDIR}/handlers/"

# Switch to the non-root user 'steam'
USER steam

# Set the working directory to the home directory of the steam user
WORKDIR ${HOMEDIR}

# Create folder for server settings and copy configuration files
RUN mkdir -p "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Master" \
             "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Caves"

COPY --chown=steam:steam "config/Cluster_1/Overworld/server.ini" "config/Cluster_1/Overworld/worldgenoverride.lua" "config/Cluster_1/Overworld/leveldataoverride.lua" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Master/"
COPY --chown=steam:steam "config/Cluster_1/Caves/server.ini" "config/Cluster_1/Caves/worldgenoverride.lua" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Caves/"
COPY --chown=steam:steam "config/Cluster_1/adminlist.txt" "config/Cluster_1/blocklist.txt" "config/Cluster_1/whitelist.txt" "config/Cluster_1/cluster.ini" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/"

# Copy mod files
COPY --chown=steam:steam "config/mods/dedicated_server_mods_setup.lua" "${STEAMAPPDIR}/mods/"
COPY --chown=steam:steam "config/mods/modsettings.lua" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Master/"
COPY --chown=steam:steam "config/mods/modsettings.lua" "${HOMEDIR}/.klei/DoNotStarveTogether/Cluster_1/Caves/"

# Set the entry point to run the health check script
ENTRYPOINT ["bash", "-c", "./entry.sh & /opt/venv/bin/python3 ./log_monitor.py --debug & /opt/venv/bin/python3 ./health_check.py"]

# Expose necessary ports
EXPOSE 11000/udp 11003/udp 8080/tcp
