from urllib import request
import re


class Spider():
    url = "https://www.panda.tv/cate/zhuji"
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<span class="video-number">([\s\S]*?)</span>'

    def __fetch_content(self):
        response = request.urlopen(Spider.url)
        htmls = response.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

    def __analysis(self, htmls):
        root_htmls = re.findall(Spider.root_pattern, htmls)
        anchors = []
        # name_htmls = re.findall(Spider.name_pattern, root_htmls)
        # number_htmls = re.findall(Spider.number_pattern, root_htmls)
        for html in root_htmls:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)
        return anchors

    def __refine(self, anchors):
        l = lambda anchor: {'name': anchor['name'][0].strip(),
                            'number': anchor['number'][0].strip()
                            }

        return map(l, anchors)

    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        r = re.findall('\d', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    def __show(self, anchors):
        for rank in range(0, len(anchors)):
            print('rank:      ' + str(rank + 1) + '主播：     ' + anchors[rank]['name']+'人数： '+ anchors[rank]['number'])
    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)


spider = Spider()
spider.go()
