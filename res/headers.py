_long_name = ('Some-long-long-long-long-long-long-long-long-long-long-long-'
              'long-long-long-long-long-long-long-long-long-long-long-long-'
              'long-long-long-long-long-long-long-header-name')
_long_value = ('Some long long long long long long long long long long long '
               'long long long long long long long long long long long long '
               'long long long long long long long long long long long long '
               'long long long long long long long long long long value')

HEADERS_LIST = [
    {},
    {'test-header': 'Some Data'},
    {'Hello': 'World', 'My-test-name': 'Contain headers'},
    {'h1': '1', 'h2': '2', 'h3': '3', 'h4': '4', 'h5': '5', 'h6': '6',
     'h7': '7'},
    {_long_name: _long_value}
]
