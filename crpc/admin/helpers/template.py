import jinja2 

class Jinja2Environment( jinja2.Environment ): 
    def load( self, template_path ): 
        tmpl = self.get_template( template_path ) 
        if tmpl: 
            setattr(tmpl, "generate", tmpl.render) 
        return tmpl 

