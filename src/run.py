import argparse, pandas as pd, matplotlib.pyplot as plt
from model import Params, Simulation

ap = argparse.ArgumentParser()
ap.add_argument('--days', type=int, default=120)
ap.add_argument('--N', type=int, default=1000)
ap.add_argument('--beta', type=float, default=0.23)
ap.add_argument('--gamma', type=float, default=0.1)
ap.add_argument('--contact-mult', type=float, default=1.0)
ap.add_argument('--mask-effect', type=float, default=0.0)
args = ap.parse_args()

p = Params(N=args.N, beta=args.beta, gamma=args.gamma,
           contact_mult=args.contact_mult, mask_effect=args.mask_effect)
sim = Simulation(p)
log = sim.run(days=args.days)

df = pd.DataFrame(log, columns=['day','S','I','R'])
df.to_csv('data/series.csv', index=False)

df.plot(x='day', y=['S','I','R'], title='SIR Time Series')
plt.savefig('figures/series.png', dpi=200)
print(df.tail())
