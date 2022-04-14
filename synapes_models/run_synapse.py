import brainpy as bp
import matplotlib.pyplot as plt


def run_syn_LIF(syn_model, run_duration=30., **kwargs):
	# 定义突触前神经元、突触后神经元和突触连接，并构建网络
	pre_neu = bp.dyn.LIF(5)
	post_neu = bp.dyn.LIF(3)
	syn = syn_model(pre_neu, post_neu, conn=bp.conn.All2All(), **kwargs)
	net = bp.dyn.Network(pre=pre_neu, syn=syn, post=post_neu)

	# 运行模拟
	runner = bp.DSRunner(net, monitors=['pre.V', 'syn.g', 'post.V'], inputs=('pre.input', 35.))
	runner(run_duration)

	# 只选取第0个突触后神经元可视化
	plt.plot(runner.mon.ts, runner.mon['syn.g'][:, 0])
	plt.xlabel('t (ms)')
	plt.ylabel('g')
	plt.show()


def run_syn(syn_model, title, run_duration=100., Iext=5., **kwargs):
	# 定义突触前神经元、突触后神经元和突触连接，并构建神经网络
	neu1 = bp.dyn.HH(1)
	neu2 = bp.dyn.HH(1)
	syn1 = syn_model(neu1, neu2, conn=bp.connect.All2All(), **kwargs)
	net = bp.dyn.Network(pre=neu1, syn=syn1, post=neu2)

	# 运行模拟
	runner = bp.dyn.DSRunner(net, inputs=[('pre.input', Iext)], monitors=['pre.V', 'post.V', 'syn.g'])
	runner.run(run_duration)

	# 可视化
	fig, gs = plt.subplots(2, 1, figsize=(6, 4.5))
	plt.sca(gs[0])
	plt.plot(runner.mon.ts, runner.mon['pre.V'], label='pre-V')
	plt.plot(runner.mon.ts, runner.mon['post.V'], label='post-V')
	plt.legend(loc='upper right')
	plt.title(title)

	plt.sca(gs[1])
	plt.plot(runner.mon.ts, runner.mon['syn.g'], label='g', color=u'#d62728')
	plt.legend(loc='upper right')

	plt.tight_layout()
	plt.show()


def run_syn_NMDA(syn_model, title, run_duration=100., Iext=5., **kwargs):
	# 定义突触前神经元、突触后神经元和突触连接，并构建神经网络
	neu1 = bp.dyn.HH(1)
	neu2 = bp.dyn.HH(1)
	syn1 = syn_model(neu1, neu2, conn=bp.connect.All2All(), **kwargs)
	net = bp.dyn.Network(pre=neu1, syn=syn1, post=neu2)

	# 运行模拟
	runner = bp.dyn.DSRunner(net,
	                         inputs=[('pre.input', Iext)],
	                         monitors=['pre.V', 'post.V', 'syn.s', 'syn.b'])
	runner.run(run_duration)

	# 可视化
	fig, gs = plt.subplots(2, 1, figsize=(6, 4.5))
	plt.sca(gs[0])
	plt.plot(runner.mon.ts, runner.mon['pre.V'], label='pre-V')
	plt.plot(runner.mon.ts, runner.mon['post.V'], label='post-V')
	plt.legend(loc='upper right')
	plt.title(title)

	plt.sca(gs[1])
	plt.plot(runner.mon.ts, runner.mon['syn.s'], label='s', color=u'#d62728')
	plt.plot(runner.mon.ts, runner.mon['syn.b'], label='b', color=u'#2ca02c')
	plt.legend(loc='upper right')

	plt.tight_layout()
	plt.show()
