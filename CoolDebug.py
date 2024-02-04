import time
import os
import sys
import re
import inspect
import subprocess
from datetime import datetime
import shutil
import difflib
_call_install = False



def _is_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        try:
            __import__(package_name.lower())
            return True
        except:
            try:
                result = subprocess.run([sys.executable, '-m','pip', 'show', '--quiet', package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                return result.returncode == 0 
            except subprocess.CalledProcessError:
                return False


def _run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"{e.stderr.strip()}")
        exit()


def _check_and_install_package(package_name):
    if not _is_package_installed("colorama"):
        _run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', 'colorama'])
    from colorama import Fore, Style
    if _is_package_installed(package_name):
        # print(f"{Fore.GREEN}[-]{Style.RESET_ALL}{package_name} is already installed")
        pass
    else:
        print(f"{Fore.BLUE}[A I P]{Style.RESET_ALL} installing {package_name}")
        if _run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', package_name]) == None:
            print(f"{Fore.RED}[A I P]{Style.RESET_ALL} {package_name} not installed")
        else:
            print(f"{Fore.GREEN}[A I P]{Style.RESET_ALL} {package_name} has been installed")



def _copy_executable_to_lib_folder():
    lib_folder = os.path.join(sys.prefix, 'Lib')
    current_executable = sys.argv[0]
    try:
        shutil.copy(current_executable, lib_folder)
        print(f"\n\nThe script is installed in your local-packages directory\nUse: {Fore.CYAN}{Style.BRIGHT}from CoolDebug import CoolDebug{Style.RESET_ALL}\n\n{Fore.BLACK}\"Note: This script cannot be used outside your local environment\"{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error on installing package on local-package:\n{e}")



html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My New Log Style</title>
<style>
body {
    font-family: 'Tahoma', sans-serif;
    background-color: #2d2d2d;
    color: #333;
    margin: 0;
    padding: 20px;
    text-align: center;
}
h1 {
    text-align: left;
    color: #c9c9c9;
    padding-bottom: 10px;
}
#debug-section {
    text-align: left;
    border: 1px solid #ddd;
    padding: 20px;
    margin-top: 20px;
    background-color: #333;
    color: #fff;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
#debug-section p {
    margin: 0;
    padding: 10px 0;
    font-size: 16px;
    color: #bcbcbc;
}
#debug-section span {
    font-weight: bold;
    color: #008080;
}
#debug-section p:nth-child(odd) {
    background-color: #444;
}
</style>
</head>
<body>
<h1>log.html from CoolDebug</h1>
<div id="debug-section">
</div>
<div id="footer">
    <p><span style='color: #969696;'>Powered by</span> <a href="https://t.me/dridop" style="color: #4158c0; text-decoration: none;">dridop</a></p>
</div>
</body>
</html>
"""

class CoolDebug:
    def __init__(self):
        self._cache = TTLCache(maxsize=5, ttl=10000)
        self.config()
    def _key_validator(valid_keys):
        def decorator(func):
            def wrapper(self, **kwargs):
                for key in kwargs.keys():
                    if key not in valid_keys:
                        closest_match = difflib.get_close_matches(key, valid_keys, n=1, cutoff=0.5)
                        if closest_match:
                            print(f'{Fore.RED}{Style.BRIGHT}Error on your Codebug Config: {Style.RESET_ALL}\nInvalid key: {Fore.RED}{key}{Style.RESET_ALL}\nDid you mean: {closest_match[0]}')
                            exit()
                        else:
                            print(f'{Fore.RED}{Style.BRIGHT}Error on your Codebug Config: {Style.RESET_ALL}\nInvalid key : {key}')
                            exit()
                return func(self, **kwargs)
            return wrapper
        return decorator
    def __format_time(self, seconds):
        if seconds < 1e-6:
            return "{:.2f} ns".format(seconds * 1e9)
        elif seconds < 1e-3:
            return "{:.2f} μs".format(seconds * 1e6)
        elif seconds < 1:
            return "{:.2f} ms".format(seconds * 1e3)
        else:
            return "{:.2f} s".format(seconds)
        

    @_key_validator(['print_log','my_timezone','show_debug','show_info','show_warning','show_error','show_critical','html_log','log_format'])
    def config(self,
    print_log=True,
    my_timezone='Asia/Tehran',
    show_debug=True,
    show_info=True,
    show_warning=True,
    show_error=True,
    show_critical=True,
    html_log=False,
    log_format='[{line_number}] [{filename}][{function}] {tag} [{timer}] > "{message}"'):
        """
## config parameters
- config you debugger as you wish with this parameters, ***`need help or have idea? <https://t.me/dridop>`_***

              
    - **log_format** = custom log format write and show 
        - {line_number} = show you the number of the line that be called
        - {filename} = show the witch python file is run and show the log
        - {function} = show you in witch function your log called 
        - {tag} = the colorfull tag to hel you know what is type of the log
        - {timer} = from the bggining the timer start and count how much time sppend 
        - {message} = show the input message
        - {year} = show year ( if your timezone be on Iran, well you have the jalali timezone)
        - {month} = show month
        - {day} = show day
        - {hour} = show hour
        - {min} = show minute
        - {sec} = show seconds
        - **default** = `[{line_number}] [{filename}][{function}] {tag} [{timer}] > "{message}"`
         
    - **print_log** = wanna see logs on your terminal?
        - default = True
         

    - **my_timezone** = custom timezone for showing in your log
        - default : 'Asia/Tehran'
         
    - **html_log** = save your log in the log.html file
        - default : False
         
    - **show_debug** = show and write debug tag log
        - default = True
         
    - **show_info** = show and write info tag log
        - default = True
         
    - **show_warning** = show and write warning tag log
        - default = True
         
    - **show_error** = show and write error tag log
        - default = True
         
    - **show_critical** = show and write critical tag log
        - default = True
         


### Example = 
#### `from CoolDebug import CoolDebug`
#### `log = CoolDebug()`
#### `log.error('my error message')`

        """
        self.show_debug = show_debug
        self.show_info = show_info
        self.show_warning = show_warning
        self.show_error = show_error
        self.show_critical = show_critical

        self.print_log = print_log
        self.html_log = html_log
        self.my_timezone = my_timezone
        if html_log != False:
            file_path = os.path.join(os.path.abspath(os.path.dirname((sys.argv[0]))), 'log.html')
            if not os.path.exists(file_path):
                with open(file_path, "w+", encoding="utf-8") as html_file:
                    html_file.write(html_content)
                if self.print_log:
                    print('HTML file {} created successfully.'.format(file_path))
        self._cache['timer'] = time.time()
        self.log_format = log_format

    def clear_cache(self):
        self._cache.clear()

    def _common_functionality(self, message, function_name, tag):
        if message is not None:
            message = str(message)
        else:
            message = ' '
        stack = inspect.stack()
        if stack:
            outer_frame = stack[-1]
            self._cache['line_number'] = str(outer_frame.lineno)
            function = stack[2].function
            function = "main" if function == "<module>" else function
            self._cache['function'] = function
            filename = os.path.basename(outer_frame.filename)
            self._cache['filename'] = '{}'.format(filename)
        self._cache['counter'] = "{}".format(self.__format_time(time.time() - self._cache['timer'])) if self._cache['timer'] else ""
        self.line_number = "{}".format(self._cache.get('line_number'))
        self.filename = "{}".format((lambda: ' ')() if self._cache.get('filename') is None else self._cache.get('filename'))
        self.function = "{}".format(self._cache.get('function'))
        self.timer = "{}".format(self._cache.get('counter'))
        self.message = message
        if function_name is not None:
            self._cache['function'] = function_name
        my_timezone = pytz.timezone(self.my_timezone)
        your_datetime = datetime.now(my_timezone)
        sec = str(your_datetime.second).zfill(2)
        min = str(your_datetime.minute).zfill(2)
        hour = str(your_datetime.hour).zfill(2)
        day = str(your_datetime.day).zfill(2)
        month = str(your_datetime.month).zfill(2)
        if my_timezone.zone == 'Asia/Tehran':
            jalali_date = JalaliDate.to_jalali(your_datetime.year, your_datetime.month, your_datetime.day)
            year = str(jalali_date.year).zfill(2)
            month = str(jalali_date.month).zfill(2)
            day = str(jalali_date.day).zfill(2)

        try:
            log_output = self.log_format.format(line_number=self.line_number, filename=self.filename, function=self.function, timer=self.timer, message=self.message, tag=tag, month=month, day=day, hour=hour, year=year, min=min, sec=sec)
        except Exception as e:
            valid_inputs = ['line_number','filename','function','timer','month','day','hour','year','min','sec']
            closest_match = difflib.get_close_matches(str(e), valid_inputs, n=1, cutoff=0.5)
            if closest_match:
                print(f'{Fore.RED}{Style.BRIGHT}Error on your Codebug Config > log_format: {Style.RESET_ALL}\nInvalid key: {Fore.RED}{e}{Style.RESET_ALL}\nDid you mean: {closest_match[0]}')
                exit()
            else:
                print(f'{Fore.RED}{Style.BRIGHT}Error on your Codebug Config > log_format: {Style.RESET_ALL}\nInvalid key : {e}')
                exit()
        return log_output

    def _insert_log_html(self, log_output, color, tag):
        file_path = os.path.join(os.path.abspath(os.path.dirname((sys.argv[0]))), 'log.html')
        if os.path.exists(file_path):
            try:
                with open(file_path, "r+", encoding="utf-8") as html_file:
                    content = html_file.read()

                    def clean_text(input_text):
                        cleaned_text = re.sub(r'<.*?>', '', input_text)
                        cleaned_text = re.sub(r'\033\[[0-9;]+m', '', cleaned_text)
                        return cleaned_text

                    log_output = clean_text(log_output)
                    insertion_point = content.find('<div id="debug-section">') + len('<div id="debug-section">')
                    prefix, keyword, rest_of_line = log_output.partition(tag)
                    html_text = "<p>{} <span style='color: {};'>{}</span>{}</p>".format(prefix, color, keyword, rest_of_line)
                    content = content[:insertion_point] + '\n {}'.format(html_text) + content[insertion_point:]
                    html_file.seek(0)
                    html_file.write(content)
                    html_file.truncate()
            except Exception as e:
                print("An error occurred: {}".format(e))
        else:
            print(f'{file_path} is not exists')
            exit()
    def debug(self, message='None', function_name=None):
        tag = "[Debug]"
        tag_name = "[Debug]"
        log_output = self._common_functionality(message, function_name, tag)
        if self.print_log != True or self.show_debug != True:
            pass
        else:
            print(log_output)
        if self.html_log:
            self._insert_log_html(log_output, '#6e6e6e', tag_name)

    def info(self, message='None', function_name=None):
        tag = "{}[Info]{}".format(Fore.GREEN, Style.RESET_ALL)
        tag_name = "[Info]"
        log_output = self._common_functionality(message, function_name, tag)
        if self.print_log != True or self.show_info != True:
            pass
        else:
            print(log_output)
        if self.html_log:
            self._insert_log_html(log_output, '#008080', tag_name)

    def warning(self, message='None', function_name=None):
        tag = "{}[Warning]{}".format(Fore.YELLOW, Style.RESET_ALL)
        tag_name = "[Warning]"
        log_output = self._common_functionality(message, function_name, tag)
        if self.print_log != True or self.show_warning != True:
            pass
        else:
            print(log_output)
        if self.html_log:
            self._insert_log_html(log_output, '#db9404', tag_name)

    def error(self, message='None', function_name=None):
        tag = "{}[Error]{}".format(Fore.RED, Style.RESET_ALL)
        tag_name = "[Error]"
        log_output = self._common_functionality(message, function_name, tag)
        if self.print_log != True or self.show_error != True:
            pass
        else:
            print(log_output)
        if self.html_log:
            self._insert_log_html(log_output, '#db2f04', tag_name)

    def critical(self, message='None', function_name=None):
        tag = "{}{}[CRITICAL]{}".format(Fore.RED, Style.BRIGHT, Style.RESET_ALL)
        tag_name = "[CRITICAL]"
        log_output = self._common_functionality(message, function_name, tag)
        if self.print_log != True or self.show_critical != True:
            pass
        else:
            print(log_output)
        if self.html_log:
            self._insert_log_html(log_output, '#000', tag_name)


if __name__ == "__main__":
    for x in range(1, len(sys.argv)):
        if sys.argv[x] == '--install':
            _check_and_install_package('colorama')
            _check_and_install_package('cachetools')
            _check_and_install_package('pytz')
            _check_and_install_package('persiantools')
            _call_install = True
            
    
#Import that packages need to install
try:
    from colorama import Fore, Style
    from cachetools import TTLCache
    import pytz
    from persiantools.jdatetime import JalaliDate
except ModuleNotFoundError as e:
    print(f'{e}\ninstall it with pip or use --install option to Auto Install')

if _call_install: _copy_executable_to_lib_folder()