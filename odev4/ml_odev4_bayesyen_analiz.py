import numpy as np
import matplotlib.pyplot as plt

try:
    import emcee
    import corner
except ImportError as exc:
    missing_name = getattr(exc, "name", "gerekli paket")
    raise SystemExit(f"{missing_name} paketi eksik. Kurulum: pip install emcee corner")

def generate_data(true_mu=150.0, true_sigma=10.0, n_obs=50, seed=42):
    rng = np.random.default_rng(seed)
    return true_mu + true_sigma * rng.standard_normal(n_obs)

def log_likelihood(theta, data):
    mu, sigma = theta
    if sigma <= 0:
        return -np.inf
    return -0.5 * np.sum(((data - mu) / sigma) ** 2 + np.log(2 * np.pi * sigma ** 2))

def log_prior(theta, mu_bounds=(0.0, 300.0), sigma_bounds=(0.0, 50.0)):
    mu, sigma = theta
    if mu_bounds[0] < mu < mu_bounds[1] and sigma_bounds[0] < sigma < sigma_bounds[1]:
        return 0.0
    return -np.inf

def log_probability(theta, data, mu_bounds=(0.0, 300.0), sigma_bounds=(0.0, 50.0)):
    lp = log_prior(theta, mu_bounds, sigma_bounds)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta, data)

def run_mcmc(data, true_mu=150.0, true_sigma=10.0, mu_bounds=(0.0, 300.0), sigma_bounds=(0.0, 50.0), initial=(140.0, 5.0), n_walkers=32, n_steps=2000, discard=500, thin=15, seed=123):
    rng = np.random.default_rng(seed)
    ndim = 2
    pos = np.array(initial, dtype=float) + 1e-4 * rng.standard_normal((n_walkers, ndim))
    sampler = emcee.EnsembleSampler(
        n_walkers,
        ndim,
        log_probability,
        args=(data, mu_bounds, sigma_bounds)
    )
    sampler.run_mcmc(pos, n_steps, progress=True)
    flat_samples = sampler.get_chain(discard=discard, thin=thin, flat=True)
    summary = summarize_samples(flat_samples, true_mu, true_sigma)
    return sampler, flat_samples, summary

def summarize_samples(samples, true_mu=150.0, true_sigma=10.0):
    names = ["mu", "sigma"]
    truths = [true_mu, true_sigma]
    result = {}
    for index, name in enumerate(names):
        q16, q50, q84 = np.percentile(samples[:, index], [16, 50, 84])
        result[name] = {
            "true": truths[index],
            "median": q50,
            "lower_16": q16,
            "upper_84": q84,
            "absolute_error": abs(q50 - truths[index]),
            "minus": q50 - q16,
            "plus": q84 - q50
        }
    return result

def print_summary(title, summary):
    print()
    print(title)
    print("Degisken,Gercek Deger,Tahmin Edilen Median,Alt Sinir %16,Ust Sinir %84,Mutlak Hata")
    for key in ["mu", "sigma"]:
        row = summary[key]
        print(
            f"{key},"
            f"{row['true']:.6f},"
            f"{row['median']:.6f},"
            f"{row['lower_16']:.6f},"
            f"{row['upper_84']:.6f},"
            f"{row['absolute_error']:.6f}"
        )

def save_summary_csv(summary, filename):
    lines = ["Degisken,Gercek Deger,Tahmin Edilen Median,Alt Sinir %16,Ust Sinir %84,Mutlak Hata"]
    for key in ["mu", "sigma"]:
        row = summary[key]
        lines.append(
            f"{key},"
            f"{row['true']:.6f},"
            f"{row['median']:.6f},"
            f"{row['lower_16']:.6f},"
            f"{row['upper_84']:.6f},"
            f"{row['absolute_error']:.6f}"
        )
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

def plot_observations(data, true_mu, filename):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(data, bins=12, alpha=0.75, edgecolor="black")
    ax.axvline(true_mu, linestyle="--", linewidth=2, label="Gercek mu")
    ax.axvline(np.mean(data), linestyle="-", linewidth=2, label="Veri ortalamasi")
    ax.set_xlabel("Parlaklik")
    ax.set_ylabel("Frekans")
    ax.set_title("Gurultulu Gozlem Verileri")
    ax.legend()
    fig.tight_layout()
    fig.savefig(filename, dpi=200)
    plt.close(fig)

def plot_corner(samples, true_mu, true_sigma, filename):
    fig = corner.corner(
        samples,
        labels=[r"$\mu$ (Parlaklik)", r"$\sigma$ (Hata)"],
        truths=[true_mu, true_sigma],
        show_titles=True,
        title_fmt=".3f"
    )
    fig.savefig(filename, dpi=200, bbox_inches="tight")
    plt.close(fig)

def plot_trace(sampler, filename):
    chain = sampler.get_chain()
    labels = [r"$\mu$", r"$\sigma$"]
    fig, axes = plt.subplots(2, figsize=(9, 6), sharex=True)
    for i in range(2):
        axes[i].plot(chain[:, :, i], alpha=0.3)
        axes[i].set_ylabel(labels[i])
    axes[-1].set_xlabel("Adim")
    fig.tight_layout()
    fig.savefig(filename, dpi=200)
    plt.close(fig)

def run_experiment(name, n_obs, mu_bounds, seed_data, seed_mcmc):
    true_mu = 150.0
    true_sigma = 10.0
    data = generate_data(true_mu=true_mu, true_sigma=true_sigma, n_obs=n_obs, seed=seed_data)
    sampler, samples, summary = run_mcmc(
        data=data,
        true_mu=true_mu,
        true_sigma=true_sigma,
        mu_bounds=mu_bounds,
        sigma_bounds=(0.0, 50.0),
        initial=(140.0, 5.0),
        n_walkers=32,
        n_steps=2000,
        discard=500,
        thin=15,
        seed=seed_mcmc
    )
    print_summary(name, summary)
    save_summary_csv(summary, f"{name}_sonuc.csv")
    plot_observations(data, true_mu, f"{name}_veri_histogrami.png")
    plot_corner(samples, true_mu, true_sigma, f"{name}_corner_plot.png")
    plot_trace(sampler, f"{name}_trace_plot.png")
    return data, sampler, samples, summary

def main():
    run_experiment("ana_senaryo_n50_genis_prior", n_obs=50, mu_bounds=(0.0, 300.0), seed_data=42, seed_mcmc=123)
    run_experiment("dar_prior_n50", n_obs=50, mu_bounds=(100.0, 110.0), seed_data=42, seed_mcmc=123)
    run_experiment("az_veri_n5_genis_prior", n_obs=5, mu_bounds=(0.0, 300.0), seed_data=42, seed_mcmc=123)

if __name__ == "__main__":
    main()
