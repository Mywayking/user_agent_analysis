import pymysql


class HtmlOutputer(object):
    def collect_data(self, data):  # 收集数据
        if data is None:
            return
        self.datas.append(data)

    def output_html(self, new_data):
        conn = pymysql.Connect(host='127.0.0.1', port=3306,
                               user='root', passwd='root', db='RTBdata', charset='utf8')
        # 使用cursor()方法获取操作游标 
        cursor = conn.cursor()
        try:
            for d in new_data:
                sql = "INSERT INTO UserAgent(UA_Company, UA_mobile, UA_OS, UA_browser, UA_UserAgent) VALUES ('%s', '%s', '%s', '%s', '%s' )" % (
                d['company'].encode('utf-8'), d['mobile'].encode('utf-8'), d['OS'].encode('utf-8'),
                d['browser'].encode('utf-8'), d['UserAgent'].encode('utf-8'))
                cursor.execute(sql)
                conn.commit()
                print("写入数据库:" + sql)
        except Exception as e:
            print("出现问题：" + str(e))
            conn.rollback()
        finally:
            conn.close()

    def output_url(self, next_url):
        fout = open("oldurl.txt", 'a')
        fout.write("%s" % next_url + "\n")
        fout.close()






        # fout = open('output.html', 'w')

        # fout.write("<html>")

        # fout.write("<head>")
        # fout.write("<meta charset= 'UTF-8'>")
        # fout.write("</head>")

        # fout.write("<body>")
        # fout.write("<table>")

        # # ASCII
        # for data in self.datas:
        #     fout.write("<tr>")
        #     fout.write("<td>%s</td>" % data['url'])
        #     fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
        #     fout.write("<td>%s</td>" % data['summary'].encode('utf-8'))
        #     fout.write("</tr>")

        # fout.write("</html>")
        # fout.write("</body>")
        # fout.write("</table>")

        # fout.close()
