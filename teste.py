# Importando bibliotecas necessárias
import osmnx as ox
import matplotlib.pyplot as plt

# Definir o local de interesse (pode ser o nome de uma cidade ou coordenadas de área)
local = "Russas, CE"

# Capturar footprints dos edifícios da cidade
# Usamos a tag 'building' para capturar apenas os edifícios
edificios = ox.features_from_place(local, tags={'building': True})

# Criar figura e eixos para plotar os edifícios
fig, ax = plt.subplots(figsize=(10, 10))
edificios.plot(ax=ax, facecolor="khaki", edgecolor="dimgray")

# Título e estilização do gráfico
ax.set_title(f"Footprints dos Edifícios em {local}", fontsize=15)

# Salvar o gráfico como imagem
plt.savefig("edificios_sao_paulo.png", dpi=300, bbox_inches='tight')

# Exibir o gráfico
plt.show()
