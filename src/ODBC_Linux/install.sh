#!/bin/bash
# HFSQL ODBC Driver V1.0 for Linux Installer
# Copyright PCSOFT.

driver_name="HFSQL ODBC Driver";
driver_short_name="HFSQL"
libdir=$(pwd)



# files to be copied by directory
driver_file_32="wd280hfo.so"
driver_file_64="wd280hfo64.so"

driver_arch=""
driver_file=""



function print_usage()
{
    echo "Usage: install.sh [options] [directory]"
    echo
    echo "Directory : directory where the driver is located. (current working dir by default)"
	echo "Options : "
    echo "   --help - prints this message"

    # don't return if we're printing the usage
    exit 0;
}



# verify that the driver manager utilities are runnable so we may
# check the configuration and install the driver.
function find_odbc_config ()
{
    echo "Verifying if iODBC is present ..."
    # see if odbc_config is installed
    hash iodbc-config &> /dev/null
    if [ $? -eq 1 ]; then
        echo "ERROR : iodbc-config from iODBC was not found.  It is required to properly install the $driver_name";
        return 1;
    fi

    return 0;
}

function check_not_installed ()
{
	echo "Checking for previous installation ..."
	local odbcinstini=$(iodbc-config --odbcinstini)
	local grepresult=$(cat $odbcinstini | grep HFSQL)

	if [ -n "$grepresult" ]; then
		echo "ERROR : $driver_name has already been installed. Please remove any references to it in $odbcinstini before reinstalling.";
		return 1;
	fi
	
	return 0;
	
}

function check_driver_present ()
{
	echo "Checking for driver ..."

	if [ -f $libdir/$driver_file ]; then
		return 0;
	fi

	echo "ERROR : Cannot find $libdir/$driver_file. Please supply a correct directory name.";
	echo "Type install.sh --help for more information";
	return 1;
}

function register_driver
{

	if check_driver_present; then
		if find_odbc_config; then
			if check_not_installed; then
				local odbcinstini=$(iodbc-config --odbcinstini)
				
				echo "Backing up odbcinst.ini to $libdir/odbcinst.ini.old ..."
				cp $odbcinstini $libdir/odbcinst.ini.old
				
				echo "Registering $driver_name ..."
				
				local grepresult=$(cat $odbcinstini | grep "ODBC Drivers")

				if [ -n "$grepresult" ]; then
					# if the ODBC Drivers section is already present, we replace its name by its name concatenated with
					# HFSQL = Installed
					sed -i -e "s/\[ODBC Drivers\]/\[ODBC Drivers\]\n$driver_short_name = Installed/g" $odbcinstini
					echo "" >> $odbcinstini
				else
					# otherwise we just add it
					echo "[ODBC Drivers]" >> $odbcinstini
					echo "$driver_short_name = Installed" >> $odbcinstini
					echo "" >> $odbcinstini
				fi

				echo "[$driver_short_name]" >> $odbcinstini
				echo "Description = $driver_name" >> $odbcinstini
				echo "Driver = $libdir/$driver_file" >> $odbcinstini
				echo "" >> $odbcinstini
				


				echo "done."
				echo""
				
				return 0;
			fi
		fi
	fi
	
}

function install()
{	
	if [ -n "$1" ]; then
		libdir=$1
	fi
	

	if [ -f $libdir/$driver_file_64 ]
	then
		driver_arch="64bit";
		driver_file=$driver_file_64 
	else
		driver_arch="32bit";
		driver_file=$driver_file_32
	fi


	echo
	echo "$driver_name ($driver_arch) Installation Script"
	echo "Copyright PCSOFT."
	echo
	echo "Starting install for $driver_name ($driver_arch)"
	echo
	register_driver $*
    return 0
}


command=$1
#shift

case "$command" in
    --help)
        print_usage
        ;;
    *)
		install $*
        ;;
esac


exit 0
