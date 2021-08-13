import cmd2
from cmd2 import (
    bg,
    fg,
    style,
)
class Cmd2EventBased(cmd2.Cmd):
    """Basic example of how to run cmd2 without it controlling the main loop."""

    def __init__(self):
        super().__init__()

    # ... your class code here ...

class BasicApp(cmd2.Cmd):
    CUSTOM_CATEGORY = 'My Custom Commands'

    def __init__(self):
        super().__init__(
            multiline_commands=['echo'],
            persistent_history_file='cmd2_history.dat',
            startup_script='scripts/startup.txt',
            include_ipy=True,
        )

        self.intro = style('Welcome to PyOhio 2019 and cmd2!', fg=fg.red, bg=bg.white, bold=True) + ' 😀'

        # Allow access to your application in py and ipy via self
        self.self_in_py = True

        # Set the default category name
        self.default_category = 'cmd2 Built-in Commands'

    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_intro(self, _):
        """Display the intro banner"""
        self.poutput(self.intro)

    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_echo(self, arg):
        """Example of a multiline command"""
        self.poutput(arg)
import collections

import aioconsole
import asyncio
from loguru import logger
import IPython
import sys
# logger.add(sys.stdout, format='>>')
# pyreadline3.
import readline
if __name__ == '__main__':
    app = BasicApp()
    # app.cmdloop()
    app.preloop()
    # app.postloop()

    async def printinfo():
        while 1:
            await asyncio.sleep(3)
            logger.info('233')
            readline.redisplay()
            # print(readline.get())
            # app.async_update_prompt('>')
            # app.precmd()
    async def readloop():
        try:
            asyncio.ensure_future(printinfo())
            # app.
            # app.cmdloop()
            while 1:
                
                res = await aioconsole.ainput('>')
                print(app.onecmd_plus_hooks(res))
        except KeyboardInterrupt:
            return
    app.postloop()
    asyncio.run(readloop())
    # app.precmd
    # app.onecmd_plus_hooks('help')
