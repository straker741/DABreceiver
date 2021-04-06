#!/bin/bash
# Make sure to leave no spaces around the equal sign.
# Otherwise, Bash will treat the variable name as a program to execute, and the = as its first parameter!


cmd="$(cat /proc/cpuinfo | grep "Raspberry Pi")"
if [[ ${#cmd} == 0 ]]
then
    echo -e "${RED_COLOUR}THIS SYSTEM IS NOT RASPBERRY PI!${DEFAULT_COLOUR}"
    exit
fi


# ----------------------------------- #
# ---------- INSTALL INPUT ---------- #
# ----------------------------------- #
APT_PACKAGES=("python3" "python3-pip" "python-dev" "python-pip" "libatlas-base-dev" "git" "cmake" "expect" "net-tools" "build-essential" "file" "rtl-sdr" "python-matplotlib" "libfftw3-dev" "librtlsdr-dev" "libfaad-dev" "libmp3lame-dev" "libmpg123-dev" "apache2" "php" "libapache2-mod-php" "php-mysql" "python-mysqldb" "python3-mysqldb" "libmysqlcppconn-dev" "python-smbus" "i2c-tools" "python3-pil" "libopenjp2-7" "mariadb-server")
PIP3_PACKAGES=("pysnmp" "uptime" "pyrtlsdr" "mysql-connector-python" "Adafruit-SSD1306")
PIP_PACKAGES=("pyrtlsdr")
SDR="Realtek Semiconductor Corp. RTL2838 DVB-T"

MY_SCRIPTS=()
MY_SCRIPTS_INFO=()
MY_SCRIPTS+=("$HOME/DABreceiver/install/change_apache2_configuration.sh")
MY_SCRIPTS_INFO+=("Apache2")
MY_SCRIPTS+=("$HOME/DABreceiver/install/mysql/mysql.sh")
MY_SCRIPTS_INFO+=("MySQL")
MY_SCRIPTS+=("$HOME/DABreceiver/install/mysql/mysql_db_user.sh")
MY_SCRIPTS_INFO+=("MySQL users")
MY_SCRIPTS+=("$HOME/DABreceiver/install/mysql/mysql_tables.sh")
MY_SCRIPTS_INFO+=("MySQL tables")
MY_SCRIPTS+=("$HOME/DABreceiver/install/enable_interfaces.sh")
MY_SCRIPTS_INFO+=("1-Wire and I2C")
MY_SCRIPTS+=("$HOME/DABreceiver/install/welle.sh")
MY_SCRIPTS_INFO+=("Welle.io")


# ------------------------------- #
# ---------- FUNCTIONS ---------- #
# ------------------------------- #
function validate_ip() {
    # source: https://www.linuxjournal.com/content/validating-ip-address-bash-script
    local  ip=$1
    local  stat=1

    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        stat=$?
    fi
    return $stat
}


# ------------------------------- #
# ---------- CONSTANTS ---------- #
# ------------------------------- #
APT_STATE=("${APT_PACKAGES[@]/*/2}")
PIP3_STATE=("${PIP3_PACKAGES[@]/*/2}")
PIP_STATE=("${PIP_PACKAGES[@]/*/2}")
MY_SCRIPTS_STATE=("${MY_SCRIPTS[@]/*/2}")

DEFAULT_COLOUR="\033[0;37m"
RED_COLOUR="\033[1;31m"
GREEN_COLOUR="\033[1;32m"
BLUE_COLOUR="\033[1;34m"
YELLOW_COLOUR="\033[1;33m"


# ------------------------------------- #
# ---------- INPUT FROM USER ---------- #
# ------------------------------------- #

# Get IPv4 address of SNMP Manager
while [[ 0 ]]
do
    echo -e "${YELLOW_COLOUR}Enter IPv4 address of SNMP Manager: ${DEFAULT_COLOUR}"
    read -p "" DABING_MANAGER_HOSTNAME
    if validate_ip $DABING_MANAGER_HOSTNAME
    then
        break
    else
        echo -e "${RED_COLOUR}Enter valid IPv4 address!${DEFAULT_COLOUR}"
    fi
done
echo -e "${GREEN_COLOUR}OK!${DEFAULT_COLOUR}"

# Get location of device for SNMP trap
echo -e "${YELLOW_COLOUR}Enter description of the location where device will be placed: ${DEFAULT_COLOUR}"
read -p "" DABING_DEVICE_LOCATION
echo -e "${GREEN_COLOUR}OK!${DEFAULT_COLOUR}"
echo ${DABING_DEVICE_LOCATION} > $HOME/DABreceiver/trapConfig.txt
echo ${DABING_MANAGER_HOSTNAME} >> $HOME/DABreceiver/trapConfig.txt

# -------------------------------------------------- #
# ---------- CONFIGURING FILE PERMISSIONS ---------- #
# -------------------------------------------------- #

# Changing the access permissions of files
chmod +x $HOME/DABreceiver/python/*
sudo chmod 666 $HOME/DABreceiver/python/bandwidth.txt


# ----------------------------------------- #
# ---------- INSTALLING PACKAGES ---------- #
# ----------------------------------------- #
echo -e "${BLUE_COLOUR}UPDATING!${DEFAULT_COLOUR}"
sudo apt-get update

echo -e "${BLUE_COLOUR}COMMENCING INSTALLATION!${DEFAULT_COLOUR}"
PAD_LENGTH=25
for INDEX in ${!APT_PACKAGES[@]}
do
    echo -e "${BLUE_COLOUR}Installing: ${APT_PACKAGES[$INDEX]}${DEFAULT_COLOUR}"
    sudo apt-get -y install ${APT_PACKAGES[$INDEX]}
    if [[ $? == 0 ]]
    then
        APT_STATE[$INDEX]=1
    else
        APT_STATE[$INDEX]=0
    fi
done

for INDEX in ${!PIP3_PACKAGES[@]}
do
    echo -e "${BLUE_COLOUR}Installing: ${PIP3_PACKAGES[$INDEX]}${DEFAULT_COLOUR}"
    pip3 install ${PIP3_PACKAGES[$INDEX]}
    if [[ $? == 0 ]]
    then
        PIP3_STATE[$INDEX]=1
    else
        PIP3_STATE[$INDEX]=0
    fi
done

for INDEX in ${!PIP_PACKAGES[@]}
do
    echo -e "${BLUE_COLOUR}Installing: ${PIP_PACKAGES[$INDEX]}${DEFAULT_COLOUR}"
    pip install ${PIP_PACKAGES[$INDEX]}
    if [[ $? == 0 ]]
    then
        PIP_STATE[$INDEX]=1
    else
        PIP_STATE[$INDEX]=0
    fi
done

# Welle.io
echo -e "${BLUE_COLOUR}Cloning Welle.io from GitHub${DEFAULT_COLOUR}"
git clone https://github.com/straker741/welle.io $HOME/DABreceiver/welle.io
if [[ $? == 0 ]]
then
    echo -e "${GREEN_COLOUR}SUCCESS${DEFAULT_COLOUR}"
else
    echo -e "${RED_COLOUR}FAIL${DEFAULT_COLOUR}"
fi

for INDEX in ${!MY_SCRIPTS[@]}
do
    echo -e "${BLUE_COLOUR}Configuring: ${MY_SCRIPTS_INFO[$INDEX]}${DEFAULT_COLOUR}"
    chmod +x ${MY_SCRIPTS[$INDEX]}
    ${MY_SCRIPTS[$INDEX]}
    if [[ $? == 0 ]]
    then
        MY_SCRIPTS_STATE[$INDEX]=1
    else
        MY_SCRIPTS_STATE[$INDEX]=0
    fi
done

# Download some data for testing
wget -c https://sdr.kt.agh.edu.pl/sdrdab-decoder/downloads/data/Record3_katowice_iq.raw -P $HOME/DABreceiver/welle.io/data/ --no-check-certificate

# radio Kraków, low noise 30-40 dB (?)
wget -c https://sdr.kt.agh.edu.pl/sdrdab-decoder/downloads/data/antena-1_dab_229072kHz_fs2048kHz_gain42_1.raw -P $HOME/DABreceiver/welle.io/data/ --no-check-certificate

echo -e "${BLUE_COLOUR}INSTALLATION FINISHED!${DEFAULT_COLOUR}\n"


for INDEX in ${!APT_STATE[@]}
do
    printf "${DEFAULT_COLOUR}Package: ${APT_PACKAGES[$INDEX]}"
    if [[ ${APT_STATE[$INDEX]} == 1 ]]
    then
        printf "%*.s ${GREEN_COLOUR}SUCCESSFULLY INSTALLED!${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#APT_PACKAGES[$INDEX]}))
    else
        printf "%*.s ${RED_COLOUR}UNSUCCESSFULLY INSTALLED!${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#APT_PACKAGES[$INDEX]}))
    fi
done

for INDEX in ${!PIP3_STATE[@]}
do
    printf "${DEFAULT_COLOUR}Package: ${PIP3_PACKAGES[$INDEX]}"
    if [[ ${PIP3_STATE[$INDEX]} == 1 ]]
    then
        printf "%*.s ${GREEN_COLOUR}SUCCESSFULLY INSTALLED!${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#PIP3_PACKAGES[$INDEX]}))
    else
        printf "%*.s ${RED_COLOUR}UNSUCCESSFULLY INSTALLED!${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#PIP3_PACKAGES[$INDEX]}))
    fi
done

for INDEX in ${!PIP_STATE[@]}
do
    printf "${DEFAULT_COLOUR}Package: ${PIP_PACKAGES[$INDEX]}"
    if [[ ${PIP_STATE[$INDEX]} == 1 ]]
    then
        printf "%*.s ${GREEN_COLOUR}SUCCESSFULLY INSTALLED!${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#PIP_PACKAGES[$INDEX]}))
    else
        printf "%*.s ${RED_COLOUR}UNSUCCESSFULLY INSTALLED!${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#PIP_PACKAGES[$INDEX]}))
    fi
done

PAD_LENGTH=21
for INDEX in ${!MY_SCRIPTS_STATE[@]}
do
    printf "${DEFAULT_COLOUR}Application: ${MY_SCRIPTS_INFO[$INDEX]}"
    if [[ ${MY_SCRIPTS_STATE[$INDEX]} == 1 ]]
    then
        printf "%*.s ${GREEN_COLOUR}SUCCESSFULLY CONFIGURED!${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#MY_SCRIPTS_INFO[$INDEX]}))
    else
        printf "%*.s ${RED_COLOUR}UNSUCCESSFULLY CONFIGURED!${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#MY_SCRIPTS_INFO[$INDEX]}))
    fi
done


# ------------------------------------ #
# ---------- HARDWARE SETUP ---------- #
# ------------------------------------ #
echo -e "${BLUE_COLOUR}LOOKING FOR CONNECTED HARDWARE!${DEFAULT_COLOUR}"
PAD_LENGTH=45

# SDR is required!
printf "Required: ${SDR}"
cmd="$(lsusb | grep "${SDR}")"
if [[ ${#cmd} != 0 ]]
then
    printf "%*.s ${GREEN_COLOUR}CONNECTED${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#SDR}))
else
    printf "%*.s ${RED_COLOUR}DISCONNECTED${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#SDR}))
fi


# --------------------------------------------- #
# ---------- SETUP FINISHED - REBOOT ---------- #
# --------------------------------------------- #
echo -e "\n${BLUE_COLOUR}REBOOT NOW? [Y/N]${DEFAULT_COLOUR}"
read -p "" REBOOT
if [[ ${REBOOT} == "Y" ]] || [[ ${REBOOT} == "y" ]]
then
    echo -e "\n${BLUE_COLOUR}REBOOTING!${DEFAULT_COLOUR}"
    sudo reboot now
else
    echo -e "\n${RED_COLOUR}REBOOT RASPBERRY BEFORE PROCEEDING!${DEFAULT_COLOUR}"
fi
