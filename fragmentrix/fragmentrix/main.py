'''
Created on 26.02.2016

@author: Yingxiong
'''
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
import numpy as np
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.properties import OptionProperty, NumericProperty, ListProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.garden.graph import Graph, MeshLinePlot
from sctt import SCTT
from kivy.core.window import Window
Window.size = (1280, 720)


class CanvasApp(App):

    sctt = SCTT()

    # update the matrix stress field
    def update_sig_m(self, *largs):
        if self.i == len(self.sctt.sig_m_K) - 1:
            return False
        self.sig_line.points = self.list_tuple(
            self.sctt.x, self.sctt.sig_m_K[self.i])
        self.i += 1

    i = 0

    # animate the cracking process
    def animate(self, *largs):
        self.sctt.get_cracking_history()
        self.i = 0
        Clock.schedule_interval(self.update_sig_m, 0.2)

    @property
    def cracking_wid(self):
        graph = Graph(xlabel='x', ylabel='matrix stress', x_ticks_minor=5,
                      x_ticks_major=100, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=0, xmax=1000, ymin=0, ymax=5)
        self.sig_mu_line = MeshLinePlot(color=[1, 0, 0, 1])
        self.sig_mu_line.points = self.list_tuple(
            self.sctt.x, self.sctt.sig_mu_x)
        self.sig_line = MeshLinePlot(color=[1, 1, 1, 1])
        graph.add_plot(self.sig_mu_line)
        graph.add_plot(self.sig_line)
        return graph

    # change bond intensity
    def set_T(self, instance, value):
        self.sctt.T = value
        self.sctt.get_sig_m_cb()
        self.cb_line.points = self.list_tuple(self.sctt.z, self.sctt.sig_m_cb)

    @property
    def cb_wid(self):
        graph = Graph(xlabel='z', ylabel='matrix stress', x_ticks_minor=5,
                      x_ticks_major=25, y_ticks_major=5,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-50, xmax=50, ymin=0, ymax=20)
        self.cb_line = MeshLinePlot(color=[1, 0, 0, 1])
        self.sctt.get_sig_m_cb()
        self.cb_line.points = self.list_tuple(self.sctt.z, self.sctt.sig_m_cb)
        graph.add_plot(self.cb_line)
        return graph

    @staticmethod
    def list_tuple(xdata, ydata):
        return list(map(tuple, np.vstack((xdata, ydata)).T))

    @property
    def curve_wid(self):
        graph = Graph(xlabel='strain', ylabel='stress',
                      x_ticks_major=0.001, y_ticks_major=2,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=0, xmax=0.01,
                      ymin=0, ymax=self.sctt.sig_cu)
        self.eps_sig_line = MeshLinePlot(color=[1, 1, 1, 1])
        self.eps_sig_line.points = self.list_tuple(
            self.sctt.eps_c_K, self.sctt.sig_c_K)
        graph.add_plot(self.eps_sig_line)
        return graph

    # plot the stress strain curve
    def plot_eps_sig(self, *largs):
        if self.sctt.sig_c_K == 0:
            self.sctt.get_cracking_history()
        self.eps_sig_line.points = self.list_tuple(
            self.sctt.eps_c_K, self.sctt.sig_c_K)

    def build(self):

        btn_animate = Button(
            text='animate', on_press=self.animate, size_hint=(0.4, 0.2))

        set_T = Slider(min=10, max=20, value=12)
        set_T.bind(value=self.set_T)

        root = TabbedPanel(do_default_tab=False)

        # cracking panel
        cracking_panel = TabbedPanelHeader(text='Cracking')
        cracking_panel.content = BoxLayout(orientation='vertical')
        cracking_panel.content.add_widget(self.cracking_wid)
        cracking_panel.content.add_widget(btn_animate)

        # cb panel
        cb_panel = TabbedPanelHeader(text='CB')
        cb_panel.content = BoxLayout()
        cb_panel.content.add_widget(self.cb_wid)
        cb_panel.content.add_widget(set_T)

        # matrix panel
        #matrix_panel = TabbedPanelHeader(text='Matrix')
        #matrix_panel = GridLayout()

        # curve panel
        btn_plot = Button(
            text='Plot', on_press=self.plot_eps_sig, size_hint=(0.4, 0.2))
        curve_panel = TabbedPanelHeader(text='Curve')
        curve_panel.content = BoxLayout(orientation='vertical')
        curve_panel.content.add_widget(self.curve_wid)
        curve_panel.content.add_widget(btn_plot)
        # curve_panel.content.add_widget(wid1)

        root.add_widget(cb_panel)
        # root.add_widget(matrix_panel)
        root.add_widget(cracking_panel)
        root.add_widget(curve_panel)

        return root

if __name__ == '__main__':
    CanvasApp().run()
