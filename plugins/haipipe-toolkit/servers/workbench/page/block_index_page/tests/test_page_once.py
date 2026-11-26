from live.page_once import once


def test_a_repeated_style_and_guarded_script_are_sent_once():
    css = "<style>.a{color:red}</style>"
    js = "<script>(function(){if(window.__x)return;window.__x=1;})();</script>"
    page = f"<p>1</p>{css}{js}<p>2</p>{css}{js}"
    out = once(page)
    assert out.count(css) == 1 and out.count(js) == 1
    assert out.index(css) < out.index("<p>2</p>")


def test_an_unguarded_script_runs_where_it_stands_every_time():
    js = "<script>document.currentScript.previousElementSibling.hidden=false</script>"
    src = '<script src="/a.js"></script>'
    page = f"<b>1</b>{js}{src}<b>2</b>{js}{src}"
    assert once(page) == page


def test_different_styles_are_all_kept():
    page = "<style>.a{}</style><style>.b{}</style>"
    assert once(page) == page
