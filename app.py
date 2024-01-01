from flask import Flask, render_template, request, send_file
from random import randint

app = Flask(__name__)


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    # print(checksum)
    return checksum % 10


def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0


def add_prefix(prefix, num):
    return int(prefix + str(num))


def add_suffix(suffix, num):
    return int(str(num) + str(suffix))


def gen_bin(n, p_card):
    n = int(n)
    i = 0
    while i != n:
        range_start = 10**(5-1)
        range_end = (10**5)-1
        f = open("./static/cards.txt", "a")

        pre_num = randint(range_start, range_end)
        num = add_prefix(p_card, pre_num)
        if p_card == 34 or 37:
            range_start = 10**(8-1)
            range_end = (10**8)-1
        else:
            range_start = 10**(10-1)
            range_end = (10**10)-1

        suff_num = randint(range_start, range_end)
        num = add_suffix(suff_num, num)

        res = is_luhn_valid(num)
        if res:
            f.write(f"{num}\n")
            i += 1
    print("Done!")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        open('./static/cards.txt', 'w').close()
        num = request.form['num']
        card_t = request.form['card_type']

        print("Generating...")
        gen_bin(num, card_t)
        path = './static/cards.txt'
        return send_file(path, as_attachment=True)

    else:
        return render_template("index.html")


# if __name__ == "__main__":
app.run(debug=True)
