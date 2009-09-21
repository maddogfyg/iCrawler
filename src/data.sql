CREATE TABLE "clawledurl" ("domainName" VARCHAR, "url" VARCHAR);
CREATE TABLE "content" ("id" INTEGER PRIMARY KEY  NOT NULL ,"url" VARCHAR,"title" VARCHAR,"content" TEXT);
CREATE TABLE "sites" ("domainName" VARCHAR PRIMARY KEY  NOT NULL , "crawlcycle" INTEGER, "lasttime" DATETIME);
CREATE TABLE sqlite_sequence(name,seq);

;mysql
CREATE TABLE `icrawler`.`clawledurl` (
`domainName` VARCHAR( 50 ) NOT NULL ,
`url` VARCHAR( 100 ) NOT NULL ,
PRIMARY KEY ( `domainName` , `url` )
) ENGINE = MYISAM 

