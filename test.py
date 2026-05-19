"""A program to display the output of the line_edits function in an
   html table.
   Originally written for COSC262 DP Assignment by Richard Lobb
   Last editted: May 2026
"""
import os
import re
from html import escape
import webbrowser
import sys

DEFAULT_CSS = """
table {font-size: 100%; border-collapse: collapse}
td, th  {border: 1px solid LightGrey; padding: 2px; }
td del {background-color: #FFBB00; text-decoration: none;}
"""

class HtmlTable:
    """A table to be rendered in HTML."""
    def __init__(self, column_headers):
        """The column headers is a list of strings. Its length determines the
           number of columns in the table"""
        self.headers = column_headers
        self.num_cols = len(column_headers)
        self._html = ""
        self._html += "<tr>" + ''.join(f"<th>{hdr}</th>" for hdr in column_headers) + "</tr>\n"

    def add_row(self, values, column_styles=None):
        """Given a list of strings ('values'), the length of which must match
           the length of the list of column headers when the table was created,
           add one row to the table. column_styles is an optional list of
           strings for setting the style attributes of the row's <td>
           elements. If given, its length must match the number of columns.

           For example
              add_row(["this", "that"], ["background-color:yellow", ""])

           would add a table row containing the values 'this' and 'that' with the
           first column having a background-color of yellow. An empty style
           string is ignored.
           String values are html-escaped (i.e. characters like '&' and '<' get
           converted to HTML-entities). Then, as a special feature for this
           assignment, any sequence of characters wrapped in double square
           brackets is instead wrapped in HTML <del> elements; these are by
           default rendered with a purple background by the HTML renderer.
           Then any newline characters are converted to <br>.
           Finally the resulting string is wrapped in a <pre> element.
        """
        def td_element(value, style, i_column):
            value = escape(value)  # HTML escaping
            value = re.sub(r'\[\[(..*?)\]\]', r'<del>\1</del>', value,
                flags=re.DOTALL + re.MULTILINE)
            value = value.replace('\n', '<br>')
            style_string = f' style="{style}"' if style else ''
            td = f"<td{style_string}><pre>{value}</pre></td>"
            return td

        if column_styles is None:
            column_styles = ["" for i in range(self.num_cols)]
        tds = [td_element(values[i], column_styles[i], i) for i in range(self.num_cols)]
        row = f"<tr>{''.join(tds)}</tr>\n"
        self._html += row

    def html(self):
        return "<table>\n" + self._html + "</table>\n"


class HtmlRenderer:
    """A class to help with displaying HTML for COSC262 DP Assignment"""
    def __init__(self, css=DEFAULT_CSS):
        """Initialise self to contain the given html string"""
        self.html = ''
        self.css = css

    def add_html(self, html):
        """Concatenate the given html to the end of the current html string"""
        self.html += html

    def render(self):
        """Display the current html in a browser window"""
        html = f"""<html><head><style>{self.css}</style></head><body>{self.html}</body></html>"""
        path = os.path.abspath('temp.html')
        with open(path, 'w') as f:
            f.write(html)
        webbrowser.open('file://' + path)


def edit_table(operations):
    """Construct an HtmlTable to display the given sequence of operations, as
       returned by the line_edits function.
    """
    table = HtmlTable(["Previous", "Current"])
    grey = "background-color:LightGrey"
    for op, left, right in operations:
        if op == 'C':
            table.add_row([left, right])
        elif op == 'D':
            table.add_row([left, right], ["background-color:#BBBBFF", grey])
        elif op == 'S':
            bg = "background-color:#FFFF99"
            table.add_row([left, right], [bg, bg])
        else:
            table.add_row([left, right], [grey, "background-color:#ABEBC6"])
    return table


#************************************************************************
#
def line_edits(s1, s2):
    s1 = s1.splitlines()
    s2 = s2.splitlines()
    memo = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    
    for i in range(len(s1)+1):
        for j in range(len(s2) + 1):
            if i == 0 and j == 0:
                continue
            if j == 0:
                memo[i][j] = i
            elif i == 0:
                memo[i][j] = j
            elif s1[i-1] == s2[j-1]:
                memo[i][j] = memo[i-1][j-1]
            else:
                memo[i][j] = 1 + min(memo[i-1][j], memo[i][j-1], memo[i-1][j-1])
    
    i = len(s1)
    j = len(s2)
    result = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i-1] == s2[j-1]:
            result.append(('C', s1[i-1], s2[j-1]))
            i -= 1
            j -= 1
        elif j == 0 or (memo[i-1][j] < memo[i-1][j-1] and memo[i-1][j] < memo[i][j-1]):
            result.append(('D', s1[i-1], ''))
            i -= 1
        elif i == 0 or (j > 0 and memo[i][j-1] < memo[i-1][j] and memo[i][j-1] < memo[i-1][j-1]):
            # Insert: ran out of s1, or insertion is cheapest
            result.append(('I', '', s2[j-1]))
            j -= 1
        else:
            # Substitute
            sub1, sub2 = identify_changes(s1[i-1], s2[j-1])
            result.append(('S', sub1, sub2))
            i -= 1
            j -= 1
    result = result[::-1]
    return result
    
def identify_changes(s1, s2):
    subsequence = lcs(s1, s2)
    r1, r2 = helper(subsequence, s1), helper(subsequence, s2)
    return r1, r2

def helper(s, seq):
    result = seq
    extras = []
    si = 0  # pointer into s (the LCS)
    for i, c in enumerate(seq):
        if si < len(s) and s[si] == c:
            si += 1
        else:
            extras.append(i)
    for i, e in enumerate(extras):
        e += 4*i
        result = result[:e] + '[[' + result[e] + ']]' + result[e+1:]
    return result
    
def lcs(s1, s2):
    memo = [[0] * (len(s2)+1) for _ in range(len(s1)+1)]
    
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                memo[i][j] = memo[i-1][j-1] + 1
            else:
                memo[i][j] = max(memo[i-1][j], memo[i][j-1])
                    
    i = len(s1)
    j = len(s2)
    result = ''
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            result += s1[i-1]
            i -= 1
            j -= 1
        else:
            if memo[i-1][j] > memo[i][j-1]:
                i -= 1
            else:
                j -= 1
    return result[::-1]
#
#************************************************************************
def line_edits(s1, s2):
    s1 = s1.splitlines()
    s2 = s2.splitlines()
    memo = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    
    for i in range(len(s1)+1):
        for j in range(len(s2) + 1):
            if i == 0 and j == 0:
                continue
            elif j == 0:
                memo[i][j] = i
            elif i == 0:
                memo[i][j] = j
            elif s1[i-1] == s2[j-1]:
                memo[i][j] = memo[i-1][j-1]
            else:
                memo[i][j] = 1 + min(memo[i-1][j], memo[i][j-1], memo[i-1][j-1])
    
    i = len(s1)
    j = len(s2)
    result = []
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            result.append(('C', s1[i-1], s2[j-1]))
            i -= 1
            j -= 1
        elif memo[i-1][j] < memo[i-1][j-1] and memo[i-1][j] < memo[i][j-1]:
            result.append(('D', s1[i-1], ''))
            i -= 1
        elif memo[i-1][j-1] < memo[i-1][j] and memo[i-1][j-1] < memo[i][j-1]:
            result.append(('S', s1[i-1], s2[j-1]))
            j -= 1
            i -=1
        else:
            result.append(('I', '', s2[j-1]))
            j -=1
    result = result[::-1]
    return result


def main(s1, s2):
    renderer = HtmlRenderer()
    renderer.add_html("<h1>Show Differences (COSC262)</h1>")
    operations = line_edits(s1, s2)
    table = edit_table(operations)
    renderer.add_html(table.html())
    renderer.render()

# Two example strings s1 and s2, follow.
# These are the same ones used in the assignment spec.

s1 = r'''# ============== DELETEs =====================
# TODO: add docstrings
@app.route('/queue/<hostname>', methods=['DELETE'])
def delete(hostname):
    try:
        data = json.loads(request.get_data())
        mac_address = data['macAddress']
    except:
        abort(400, 'Missing or invalid user data')
    status = queue.dequeue(hostname, macAddress)
    return ('', status)


@app.route('/queue', methods=['DELETE'])
def empty_queue():
    if request.remote_addr.upper() != TUTOR_MACHINE.upper():
        abort(403, "Not authorised")
    else:
        queue.clear_queue()
        response = jsonify({"message": "Queue emptied"})
        response.status_code = 204
        return response
'''

s2 = r'''# ============== DELETEs =====================
@app.route('/queue/<hostname>', methods=['DELETE'])
def delete(hostname):
    """Handle delete request from the given host"""
    try:
        data = json.loads(request.get_data())
        mac_address = data['mac_address']
    except:
        abort(400, 'Missing or invalid user data')
    status = queue.dequeue(hostname, mac_address)
    return ('', status)


@app.route('/queue', methods=['DELETE'])
def clear_queue():
    """Clear the queue. Valid only if coming from tutor machine"""
    if request.remote_addr.upper() != TUTOR_MACHINE.upper():
        abort(403, "Only the tutor machine can clear the queue")
    else:
        queue.clear_queue()
        response = jsonify({"message": "Queue cleared"})
        response.status_code = 204
        return response
'''


main(s1, s2)
