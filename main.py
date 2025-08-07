from plugins.light_model import LightModelPlugin

plugin = LightModelPlugin()
plugin.load_model()
output = plugin.run("sample data")
print(output)
