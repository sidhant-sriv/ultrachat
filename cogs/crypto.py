from discord.ext import commands
import hashlib
import base64


class CaeserCipher:

    def encrypt(self, text, key=3):
        result = ""
        for i in text:
            if i.isupper():
                result += chr((ord(i)+key-65) % 26+65)
            elif i.islower():
                result += chr((ord(i)+key-97) % 26+97)
            else:
                result += i
        return result

    def decrypt(self, text, key=3):
        result = ""
        for i in text:
            if i.isupper():
                result += chr((ord(i)-key-65) % 26+65)
            elif i.islower():
                result += chr((ord(i)-key-97) % 26+97)
            else:
                result += i
        return result


class SHA256:
    def __init__(self, text):
        self.text = text
        self.hash = hashlib.sha256(text.encode('utf-8')).hexdigest()

    def __str__(self):
        return self.hash

    def __repr__(self):
        return self.hash


class MD5:
    def __init__(self, text):
        self.text = text
        self.hash = hashlib.md5(text.encode('utf-8')).hexdigest()

    def __str__(self):
        return self.hash

    def __repr__(self):
        return self.hash


class Cryptography(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="caeser_e")
    async def caeser_e(self, ctx, *, text):
        '''Returns the caeser cipher encrypted message'''
        await ctx.send("```{}```".format(CaeserCipher().encrypt(text)))

    @commands.command(name="caeser_d")
    async def caeser_d(self, ctx, key, *, text):
        '''Returns the caeser cipher decrypted message'''
        await ctx.send("```{}```".format(CaeserCipher().decrypt(text, int(key))))

    @commands.command(name='sha256')
    async def sha256(self, ctx, *, text):
        '''Returns a sha256 hash of message'''
        await ctx.send("`SHA256 Hash: {}`".format(SHA256(text)))

    @commands.command(name='md5')
    async def md5(self, ctx, *, text):
        '''Returns a md5 hash of message'''
        await ctx.send("MD5 Hash: `{}`".format(MD5(text)))

    @commands.command(name='base64_e')
    async def base64_e(self, ctx, *, text):
        "Returns a base64 encoded message"
        await ctx.send("```{}```".format(base64.b64encode(text.encode('utf-8')).decode('utf-8')))

    @commands.command(name='base64_d')
    async def base64_d(self, ctx, *, text):
        "Returns a base64 decrypted message"
        await ctx.send("```{}```".format(base64.b64decode(text.encode('utf-8')).decode('utf-8')))


async def setup(bot):
    await bot.add_cog(Cryptography(bot))
