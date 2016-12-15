# !/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser


def main():
    parser = OptionParser(usage='')
    parser.add_option('-r', '--range', type='int', help='')
    parser.add_option('-u', '--units', type='string', help='')
    parser.add_option('-t', '--transport', type='string', help='')
    parser.add_option('-f', '--file', type='string', help='')
    
    (options, args) = parser.parse_args()
    
    if not options.range:
        parser.error('Range is required')
    if not options.units:
        parser.error('Units are required [\'sec\', \'meter\']')
    if options.units not in ['sec', 'meter']:
        parser.error('Invalid units type [\'sec\', \'meter\']')
    if not options.transport:
        parser.error('Transport type is required [\'pedestrian\', \'bike\', \'car\']')
    if options.transport not in ['pedestrian', 'bike', 'car']:
        parser.error('Invalid units type [\'pedestrian\', \'bike\', \'car\']')
    
    print options
    print args

         
if __name__ == '__main__':
    main()