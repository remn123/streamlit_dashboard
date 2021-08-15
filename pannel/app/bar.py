import altair as alt


class BarPlot():

    def __init__(self, width=None, height=None):
        self.width = width
        self.height = height

    def compute(self, source):
        base = self._make_base(source)
        
        bars = base.facet(
            column=alt.Column(
                'index', 
                header=alt.Header(
                    title='Plot', 
                    titleColor='white',
                    titleFontSize=24,
                    labelColor='white', 
                    labelOrient='top',
                    labelFontSize=24
                )
            ),
        ).resolve_scale(
            x='independent'
        )
        return bars


    def _make_base(self, source):
        base = alt.Chart(source).mark_bar().encode(
            x=alt.X(
                'variable:N',
                sort='-y',
                axis=alt.Axis(title=None, labelAngle=0),
            ),
            y=alt.Y(
                'value:Q',
                axis=alt.Axis(
                    title=None,
                    labelFontSize=18, 
                    titleAngle=0
                ),
            ),
            color=alt.Color(
                'variable', 
                title='Clientes',
                scale=alt.Scale(scheme='pastel1')

            ),
            tooltip=[
                alt.Tooltip('variable:N', title='Cliente: '),
                alt.Tooltip('value:Q', title='Valor: ', format=',.2r'),
            ]
        ).properties(
            width=530
        )
        
        return base