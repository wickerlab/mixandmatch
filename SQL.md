## Windows
1. MySQL Download: MySQL :: Download MySQL Community Server  
   Follow configuration and remember the root password you make (necessary later)

2. Start SQL: Windows: Services -> start MySQL 

3. Login to your root user for SQL and set up mixnmatch user
    `mysql -u root -p`

    `CREATE USER 'mixnmatch'@'localhost' IDENTIFIED BY 'mixnmatch';`

    `GRANT ALL PRIVILEGES ON *.* TO 'mixnmatch'@'localhost' WITH GRANT OPTION;`

    `FLUSH PRIVILEGES;`

 

4. Open new terminal and sign into the new mixnmatch account, and create database + tables: 

    `mysql -u mixnmatch -p`
    (password is: mixnmatch)

    `CREATE DATABASE mixnmatch;`

    `USE mixnmatch;`

    `source \path\to\mixnmatch_repo\backend_mm\mysql_database\dump.sql`
 

## Mac
1. Install homebrew if not already installed

    `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

2. Install MySQL using homebrew and start it
    `brew install mysql`

    `brew services start mysql`

3. Login to your root user for SQL and set up mixnmatch user

    `mysql mysql -u root -p`

    `CREATE USER 'mixnmatch'@'localhost' IDENTIFIED BY 'mixnmatch';`

    `GRANT ALL PRIVILEGES ON *.* TO 'mixnmatch'@'localhost' WITH GRANT OPTION;`

    `FLUSH PRIVILEGES;`

 
4. Open new terminal and sign into the new mixnmatch account, and create database + tables: 

    `mysql -u mixnmatch -p`
    (password is: mixnmatch)

    `CREATE DATABASE mixnmatch;`

    `USE mixnmatch;`

    `source \path\to\mixnmatch_repo\backend_mm\mysql_database\dump.sql`