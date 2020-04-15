#!/usr/bin/expect
spawn mysql -u stu -p
expect "Enter password:"
send "korona2020\n"

expect "MariaDB \\\[(none)]>"
send "USE bakalarka;\n"
expect "MariaDB \\\[bakalarka]>"
send "CREATE TABLE IF NOT EXISTS biterrorratio ( id int not null auto_increment primary key, value REAL(11,10), datetime timestamp DEFAULT current_timestamp );\n"
expect "MariaDB \\\[bakalarka]>"
send "CREATE TABLE IF NOT EXISTS signaltonoiseratio ( id int not null auto_increment primary key, value REAL(13,10), datetime timestamp DEFAULT current_timestamp );\n"
expect "MariaDB \\\[bakalarka]>"
send "CREATE TABLE IF NOT EXISTS fiberrorratio ( id int not null auto_increment primary key, value REAL(13,10), datetime timestamp DEFAULT current_timestamp );\n"
expect "MariaDB \\\[bakalarka]>"
send "CREATE TABLE IF NOT EXISTS temperature ( id int not null auto_increment primary key, temp REAL(6,3), datetime timestamp DEFAULT current_timestamp );\n"
expect "MariaDB \\\[bakalarka]>"
send "quit\n"