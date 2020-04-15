#!/usr/bin/expect
spawn sudo mysql -u root -p
expect "Enter password:"
send "korona2020\n"

expect "MariaDB \\\[(none)]>"
send "CREATE DATABASE IF NOT EXISTS bakalarka;\n"
expect "MariaDB \\\[(none)]>"
send "CREATE USER 'stu'@'localhost' IDENTIFIED BY 'korona2020';\n"
expect "MariaDB \\\[(none)]>"
send "GRANT ALL PRIVILEGES ON bakalarka.* TO 'stu'@'localhost';\n"
expect "MariaDB \\\[(none)]>"
send "FLUSH PRIVILEGES;\n"
expect "MariaDB \\\[(none)]>"
send "quit\n"