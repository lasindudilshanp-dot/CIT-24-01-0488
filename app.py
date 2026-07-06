from flask import Flask, request, render_template_string
import redis
import os

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Note App</title>
<style>body{font-family:sans-serif;max-width:600px;margin:40px auto;padding:0 20px}</style>
</head>
<body>
<h1>📝 Notes App</h1>
<form method="POST" action="/add">
  <input name="note" placeholder="Write a note..." style="width:80%;padding:8px">
  <button type="submit">Add</button>
</form>
<hr>
<h2>All Notes</h2>
{% for note in notes %}
  <p>• {{ note }}</p>
{% else %}
  <p>No notes yet.</p>
{% endfor %}
</body>
</html>
"""

@app.route('/')
def index():
    notes = r.lrange('notes', 0, -1)
    return render_template_string(HTML, notes=notes)

@app.route('/add', methods=['POST'])
def add():
    note = request.form.get('note', '').strip()
    if note:
        r.lpush('notes', note)
    from flask import redirect
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
