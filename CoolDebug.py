import time
import os
import sys
import re
import inspect
import subprocess
from datetime import datetime
import shutil
import difflib
from functools import lru_cache
import atexit




__call_install = False

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
        print(f"{Fore.BLUE}[AIP]{Style.RESET_ALL} installing {package_name}")
        if _run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', package_name]) == None:
            print(f"{Fore.RED}[AIP]{Style.RESET_ALL} {package_name} not installed")
        else:
            print(f"{Fore.GREEN}[AIP]{Style.RESET_ALL} {package_name} has been installed")


def _copy_executable_to_lib_folder():
    command = [sys.executable, '-m', 'pip', 'show', 'pip']
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            location_line = next(line for line in result.stdout.split('\n') if line.startswith('Location:'))
            pip_location = location_line.split(':', 1)[1].strip()
        else:
            print(f"Error: {result.stderr.strip()}")
            exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()

    current_executable = sys.argv[0]
    program_name_with_extension = os.path.basename(current_executable)
    program_name = os.path.splitext(program_name_with_extension)[0]
    package_folder_path = os.path.join(pip_location, program_name)

    try:
        os.makedirs(package_folder_path, exist_ok=True)
        target_file_path = os.path.join(package_folder_path, '__init__.py')
        if os.path.exists(target_file_path):
            os.remove(target_file_path)
        shutil.copy(current_executable, package_folder_path)
        new_file_path = os.path.join(package_folder_path, '__init__.py')
        os.rename(os.path.join(package_folder_path, os.path.basename(current_executable)), new_file_path)
        print(f"\n\nThe script is installed in your local-packages {package_folder_path}\n"
              f"Use: {Fore.CYAN}{Style.BRIGHT}from CoolDebug import CoolDebug{Style.RESET_ALL}\n"
              f"\n{Fore.BLACK}\"Note: This script cannot be used outside your local environment\"{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error on installing package on local-package:\n{e}")


def _cleanup():
    try:
        file_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'log.html')
        if file_path:
            with open(file_path, "r+", encoding="utf-8") as html_file:
                content = html_file.read()
                if not content.endswith("</html>"):
                    html_text = '''
</div>
<div id="footer">
<p><span style='color: #969696;'>Powered by</span> <a href="https://t.me/dridop" style="color: #4158c0; text-decoration: none;">dridop</a></p>
</div>
</body>
</html>'''
                    html_file.write(f"\n{html_text}")
        else:
            print("Error: 'file_path' variable is not set correctly.")
    except Exception as e:
        print(f"An error occurred: {e}")
    try:
        shutil.rmtree(os.path.join(os.path.abspath(os.path.dirname((sys.argv[0]))), '__pycache__'))
    except:
        pass

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

"""

class CoolDebug:
    def __init__(self):
        self.config()
        if not os.environ.get('CoolDebug_timer'):
            os.environ['CoolDebug_timer'] = str(time.time())
    
    def __key_validator(valid_keys):
        def decorator(func):
            def wrapper(self, **kwargs):
                for key in kwargs.keys():
                    if key not in valid_keys:
                        closest_match = difflib.get_close_matches(key, valid_keys, n=1, cutoff=0.5)
                        if closest_match:
                            print(f'{Fore.RED}{Style.BRIGHT}Error on your CoolDebug Config: {Style.RESET_ALL}\nInvalid key: {Fore.RED}{key}{Style.RESET_ALL}\nDid you mean: {closest_match[0]}')
                            exit()
                        else:
                            print(f'{Fore.RED}{Style.BRIGHT}Error on your CoolDebug Config: {Style.RESET_ALL}\nInvalid key : {key}')
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
        
    @__key_validator(['print_log','my_timezone','show_debug','show_info','show_warning','show_error','show_critical','html_log','log_format'])
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
        - {msec} = show miliseconds
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
        self.__show_debug = show_debug
        self.__show_info = show_info
        self.__show_warning = show_warning
        self.__show_error = show_error
        self.__show_critical = show_critical
        self.__print_log = print_log
        self.__html_log = html_log
        self.__my_timezone = my_timezone
        self.__log_format = log_format

        if html_log == True:
            os.environ['html_file_true'] = 'True'
            html_file_path = os.path.join(os.path.abspath(os.path.dirname((sys.argv[0]))), 'log.html')
            os.environ['html_file_path'] = html_file_path
            if not os.path.exists(html_file_path):
                with open(html_file_path, "w+", encoding="utf-8") as html_file:
                    html_file.write(html_content)
                if self.__print_log:
                    print('HTML file {} created successfully.'.format(html_file_path))
            else:
                try:
                    with open(html_file_path, 'rb+') as file:
                            file.seek(0, 2)
                            end_position = file.tell()
                            lines_count = 0
                            while end_position > 0 and lines_count < 6:
                                end_position -= 1
                                file.seek(end_position)
                                current_byte = file.read(1)
                                if current_byte == b'\n':
                                    lines_count += 1
                                file.truncate(end_position)
                except Exception as e:
                    print(f"An error occurred: {e}")
    
    @lru_cache(maxsize=None)
    def __common_functionality(self, message, function_name, tag):
        message = str(message)
        stack = inspect.stack()
        outer_frame = stack[2]
        line_number = str(outer_frame.lineno)
        function = outer_frame.function
        function = "main" if function == "<module>" else function
        filename = os.path.basename(outer_frame.filename)
        timer = float(os.environ.get('CoolDebug_timer'))
        counter = self.__format_time(time.time() - timer)
        function = function_name if function_name is not None else function
        my_timezone = timezone(self.__my_timezone)
        your_datetime = datetime.now(my_timezone)
        
        msec, sec, min, hour, day, month = map(lambda x: str(x).zfill(2), [f"{your_datetime.strftime('%f')[:3]}",your_datetime.second, your_datetime.minute, your_datetime.hour, your_datetime.day, your_datetime.month])
        if my_timezone.zone == 'Asia/Tehran':
            jalali_date = JalaliDate.to_jalali(your_datetime.year, your_datetime.month, your_datetime.day)
            year, month, day = map(lambda x: str(x).zfill(2), [jalali_date.year, jalali_date.month, jalali_date.day])
        try:
            log_output = self.__log_format.format(line_number=line_number, filename=filename, function=function, timer=counter, message=message, tag=tag, month=month, day=day, hour=hour, year=year, min=min, sec=sec,msec=msec)
        except Exception as e:
            valid_inputs = ['msec','line_number','filename','function','timer','month','day','hour','year','min','sec']
            closest_match = difflib.get_close_matches(str(e), valid_inputs, n=1, cutoff=0.5)
            if closest_match:
                print(f'{Fore.RED}{Style.BRIGHT}Error on your Codebug Config > log_format: {Style.RESET_ALL}\nInvalid key: {Fore.RED}{e}{Style.RESET_ALL}\nDid you mean: {closest_match[0]}')
                exit()
            else:
                print(f'{Fore.RED}{Style.BRIGHT}Error on your Codebug Config > log_format: {Style.RESET_ALL}\nInvalid key : {e}')
                exit()
        return log_output
    


    @lru_cache(maxsize=None)
    def __insert_log_html(self, log_output, color, tag):
        file_path = os.environ.get('html_file_path')

        if os.path.exists(file_path):
            try:
                with open(file_path, "a", encoding="utf-8") as html_file:
                    def clean_text(input_text):
                        return re.sub(r'<.*?>|\033\[[0-9;]+m', '', input_text)

                    log_output = clean_text(log_output)
                    prefix, keyword, rest_of_line = log_output.partition(tag)
                    html_text = f"<p>{prefix} <span style='color: {color};'>{keyword}</span>{rest_of_line}</p>"

                    html_file.write(f"\n {html_text}")
            except Exception as e:
                print("An error occurred: {}".format(e))
        else:
            print(f'{file_path} is not exists')
    
    def debug(self, message='None', function_name=None):
        "show debug type message with tag [Debug]"
        tag = "[Debug]"
        tag_name = "[Debug]"
        log_output = self.__common_functionality(message, function_name, tag)
        if self.__print_log != True or self.__show_debug != True:
            pass
        else:
            print(log_output)
        if self.__html_log:
            self.__insert_log_html(log_output, '#6e6e6e', tag_name)

    def info(self, message='None', function_name=None):
        "show info type message with tag [Info]"
        tag = "{}[Info]{}".format(Fore.GREEN, Style.RESET_ALL)
        tag_name = "[Info]"
        log_output = self.__common_functionality(message, function_name, tag)
        if self.__print_log != True or self.__show_info != True:
            pass
        else:
            print(log_output)
        if self.__html_log:
            self.__insert_log_html(log_output, '#008080', tag_name)

    def warning(self, message='None', function_name=None):
        "show warning type message with tag [Warning]"
        tag = "{}[Warning]{}".format(Fore.YELLOW, Style.RESET_ALL)
        tag_name = "[Warning]"
        log_output = self.__common_functionality(message, function_name, tag)
        if self.__print_log != True or self.__show_warning != True:
            pass
        else:
            print(log_output)
        if self.__html_log:
            self.__insert_log_html(log_output, '#db9404', tag_name)

    def error(self, message='None', function_name=None):
        "show error type message with tag [Error]"
        tag = "{}[Error]{}".format(Fore.RED, Style.RESET_ALL)
        tag_name = "[Error]"
        log_output = self.__common_functionality(message, function_name, tag)
        if self.__print_log != True or self.__show_error != True:
            pass
        else:
            print(log_output)
        if self.__html_log:
            self.__insert_log_html(log_output, '#db2f04', tag_name)

    def critical(self, message='None', function_name=None):
        "show critical type message with tag [CRITICAL]"
        tag = "{}{}[CRITICAL]{}".format(Fore.RED, Style.BRIGHT, Style.RESET_ALL)
        tag_name = "[CRITICAL]"
        log_output = self.__common_functionality(message, function_name, tag)
        if self.__print_log != True or self.__show_critical != True:
            pass
        else:
            print(log_output)
        if self.__html_log:
            self.__insert_log_html(log_output, '#000', tag_name)



if __name__ == "__main__":
    for x in range(1, len(sys.argv)):
        if sys.argv[x] == '--install':
            _check_and_install_package('colorama')
            _check_and_install_package('pytz')
            _check_and_install_package('persiantools')
            __call_install = True
    
try:
    from colorama import Fore, Style
    from pytz import timezone
    from persiantools.jdatetime import JalaliDate
except ModuleNotFoundError as e:
    print(f'{e}\ninstall it with pip or use --install option to Auto Install')

if __call_install: _copy_executable_to_lib_folder()
atexit.register(_cleanup)
