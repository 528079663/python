# -*- coding: utf-8 -*-
import scrapy
import pymysql as mysql


def mysql_insert(sql):
    ip = 'localhost'
    user = 'root'
    password = 'root'
    port = '3306'
    schema = 'my'
    db = mysql.connect(ip, user, password, schema)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        return 'success'
    except:
        db.rollback()
        return 'failed'
    db.close()


class ShuangseqiuSpiderSpider(scrapy.Spider):
    name = 'shuangseqiu_spider'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['http://kaijiang.500.com/shtml/ssq/18000.shtml']

    def start_requests(self):
        start_num = 19200
        prefix = 'http://kaijiang.500.com/shtml/ssq/'
        tailfix = '.shtml'
        for i in range(18000, start_num):
            url = prefix + str(i) + tailfix
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        ball_red = response.xpath('//li[@class = "ball_red"]/text()').extract()
        ball_blue = response.xpath('//li[@class = "ball_blue"]/text()').extract()
        circle = response.url[34:39]
        ball_red = ','.join(ball_red)
        ball_blue = ','.join(ball_blue)
        print(ball_red)
        print(ball_blue)
        print(circle)
        sql = "INSERT INTO my.shuangseqiu (red,blue,circle) VALUES (" + '\'' + ball_red + '\',\'' + ball_blue + '\',' + circle + ")"
        print(sql)
        mysql_insert(sql)
