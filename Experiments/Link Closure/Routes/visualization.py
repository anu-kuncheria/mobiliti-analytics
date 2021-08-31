import analysis_tools

# Plot in Kepler
normal55k = pd.DataFrame([(i, j) for i, j in normallinks_55k.items()],
                   columns=["link_id", "Count"])
normal55k_geom = kepler_geom(normal55k,sf_links,os.path.join(path,'sf_nodes.csv'))
normal55k_geom.to_csv('normal_rsr.csv', index = False)
