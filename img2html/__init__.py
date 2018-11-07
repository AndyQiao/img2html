from trans import Trans
import argparse


parser = argparse.ArgumentParser(description='img2html : Convert image to HTML')
parser.add_argument('-b', '--background', default='000000', metavar='#RRGGBB',
                    help='background color (#RRGGBB format)')
parser.add_argument('-s', '--size', default=10, type=int, metavar='(4~30)',
                    help='font size (int)')
parser.add_argument('-c', '--char', default='囧', metavar='CHAR',
                    help='characters')
parser.add_argument('-t', '--title', default='img2html by qiaoconglovelife@163.com', metavar='TITLE',
                    help='html title')
parser.add_argument('-f', '--font', default='monospace', metavar='FONT',
                    help='html font')
parser.add_argument('-i', '--input', metavar='IN', help='image to convert', required=True)
parser.add_argument('-o', '--output', default=None, metavar='OUT',
                    help='output file')

args,text = parser.parse_known_args()

trans = Trans(args.size,
              args.background,
              args.title,
              args.font
)
trans.trans(args.input, args.char)



