# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SlPipeline(object):
    def process_item(self, item, spider):
        return item


class HotelreviewsPipeline(object):
    def process_item(self, item, spider):
        return item


# # FROM AIRLINE RUN
#
# # -*- coding: utf-8 -*-
#
# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#
# from scrapy.exceptions import DropItem
# from scrapy.exporters import CsvItemExporter
#
# class ValidateItemPipeline(object):
#
#     def process_item(self, item, spider):
#         if not all(item.values()):
#             raise DropItem("Missing values!")
#         else:
#             return item
#
# class WriteItemPipeline(object):
#
#     def __init__(self):
#         self.filename = 'reviews4.csv'
#
#     def open_spider(self, spider):
#         self.csvfile = open(self.filename, 'wb')
#         self.exporter = CsvItemExporter(self.csvfile)
#         self.exporter.start_exporting()
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.csvfile.close()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
