# -----------------------------
# Clear environment and load libraries
# -----------------------------
rm(list = ls())
library(tidyverse)
library(ggtree)
library(treeio)
library(ape)
library(phytools)

# -----------------------------
# Config paths
# -----------------------------
input_file <- "OG0000195_clean2_mafft_80trim"
phyl_dir <- "phylogeny_analysis"
pipeline_dir <- file.path(phyl_dir, "puhti")
tree_dir <- file.path(pipeline_dir, "iqtree_files")

tree_file <- file.path(tree_dir, paste0(input_file, ".treefile"))
septin_file <- file.path(phyl_dir, "Septins.csv")
tax_file <- "proteome_list_orthofinder.csv"
tax_outgroup_file <- file.path(phyl_dir, "outgroup_phylogeny.csv")
output_tree <- file.path(tree_dir, paste0(input_file, ".pdf"))
output_node_tree <- file.path(tree_dir, paste0(input_file, "_nodes.pdf"))

# -----------------------------
# Load tree and root
# -----------------------------
stopifnot(file.exists(tree_file), file.exists(septin_file), 
          file.exists(tax_file), file.exists(tax_outgroup_file))

tree <- read.tree(tree_file)
stopifnot(!is.null(tree), length(tree$tip.label) > 0)

# Root by priority
if ("Sacce1-Myo2" %in% tree$tip.label) {
  tree <- root(tree, outgroup = "Sacce1-Myo2", resolve.root = TRUE)
} else if ("Dicdi-GtpA" %in% tree$tip.label) {
  tree <- root(tree, outgroup = "Dicdi-GtpA", resolve.root = TRUE)
} else {
  tree <- midpoint.root(tree)
}

# -----------------------------
# Load and process metadata
# -----------------------------
tax_data <- read.csv(tax_file) %>%
  full_join(read.csv(tax_outgroup_file)) %>%
  select(portal, name, phylum:genus) %>%
  mutate(portal = as.character(portal))

char_septins <- read.csv(septin_file)
stopifnot(all(c("protein_id", "new_id") %in% names(char_septins)))

# Rename tips
label_map <- setNames(tree$tip.label, tree$tip.label)
matches <- char_septins$protein_id %in% tree$tip.label
label_map[char_septins$protein_id[matches]] <- char_septins$new_id[matches]
tree$tip.label <- unname(label_map[tree$tip.label])

# Annotate tip metadata
tip_metadata <- data.frame(label = tree$tip.label) %>%
  mutate(portal = str_split_i(label, "-", 1)) %>%
  left_join(tax_data, by = "portal")

# Attach to tree
tree_gg <- ggtree(tree) %<+% tip_metadata
tree_phylo <- tree

# -----------------------------
# Save tree with node numbers
# -----------------------------
ggsave(output_node_tree,
       tree_gg +
         geom_tippoint(aes(color = phylum), size = 2) +
         geom_tiplab(size = 2) +
         geom_nodelab(aes(label = node), size = 2, nudge_x = 0.01, nudge_y = 0.5) +
         theme_tree2() +
         theme(legend.position = "right"),
       width = 20, height = 50, limitsize = FALSE)

# -----------------------------
# Descendant helper
# -----------------------------
getDescendants <- function(tree, node) {
  kids <- tree$edge[tree$edge[, 1] == node, 2]
  desc <- kids
  for (k in kids) {
    if (k > length(tree$tip.label)) {
      desc <- c(desc, getDescendants(tree, k))
    }
  }
  return(desc)
}

# -----------------------------
# Detect monophyletic class clades
# -----------------------------
annotation_class <- "class"
tip_info_class <- tree_gg$data %>% filter(isTip) %>% select(label, !!sym(annotation_class))
internal_nodes <- (length(tree_phylo$tip.label) + 1):max(tree_phylo$edge)
clade_labels <- list()

for (node in internal_nodes) {
  desc <- getDescendants(tree_phylo, node)
  tips <- desc[desc <= length(tree_phylo$tip.label)]
  labels <- tree_phylo$tip.label[tips]
  vals <- tip_info_class %>% filter(label %in% labels) %>% pull(!!sym(annotation_class)) %>% unique()
  if (length(vals) == 1 && !is.na(vals)) {
    clade_labels[[length(clade_labels) + 1]] <- list(node = node, label = vals)
  }
}

# Remove nested class clades
filtered_class <- list()
for (i in seq_along(clade_labels)) {
  cur <- clade_labels[[i]]
  nested <- any(sapply(clade_labels, function(other) {
    cur$label == other$label &&
      cur$node != other$node &&
      cur$node %in% getDescendants(tree_phylo, other$node)
  }))
  if (!nested) filtered_class[[length(filtered_class) + 1]] <- cur
}
cat("Found", length(filtered_class), "non-nested class clades.\n")

# -----------------------------
# Detect monophyletic phylum clades for branch coloring
# -----------------------------
annotation_phylum <- "phylum"
tip_info_phylum <- tree_gg$data %>% filter(isTip) %>% select(label, !!sym(annotation_phylum))

filtered_phylum <- list()
for (node in internal_nodes) {
  desc <- getDescendants(tree_phylo, node)
  tips <- desc[desc <= length(tree_phylo$tip.label)]
  labels <- tree_phylo$tip.label[tips]
  vals <- tip_info_phylum %>% filter(label %in% labels) %>% pull(!!sym(annotation_phylum)) %>% unique()
  if (length(vals) == 1 && !is.na(vals)) {
    filtered_phylum[[length(filtered_phylum) + 1]] <- list(node = node, phylum = vals)
  }
}

# Include singleton tips for branch coloring
singleton_tips <- tree_gg$data %>% filter(isTip, !is.na(phylum))
for (i in seq_len(nrow(singleton_tips))) {
  tip_node <- singleton_tips$node[i]
  phylum <- singleton_tips$phylum[i]
  filtered_phylum[[length(filtered_phylum) + 1]] <- list(node = tip_node, phylum = phylum)
}

# Remove nested phylum clades
filtered_phylum_final <- list()
for (i in seq_along(filtered_phylum)) {
  cur <- filtered_phylum[[i]]
  nested <- any(sapply(filtered_phylum, function(other) {
    cur$phylum == other$phylum &&
      cur$node != other$node &&
      cur$node %in% getDescendants(tree_phylo, other$node)
  }))
  if (!nested) filtered_phylum_final[[length(filtered_phylum_final) + 1]] <- cur
}

# -----------------------------
# Color assignment
# -----------------------------
branch_df <- tree_gg$data
branch_df$branch_color <- "black"

# Colorblind-safe palette
phylum_palette <- c(
  "Ascomycota" = "#E69F00",
  "Basidiomycota" = "#56B4E9",
  "Mucoromycota" = "#009E73",
  "Glomeromycota" = "#F0E442",
  "Chytridiomycota" = "#0072B2",
  "Blastocladiomycota" = "#D55E00",
  "Evosea" = "#000000"
)

phylum_names <- unique(unlist(lapply(filtered_phylum_final, `[[`, "phylum")))
phylum_colors <- phylum_palette[phylum_names]

# Apply branch colors and build legend factor
branch_df$phylum_legend <- NA
for (clade in filtered_phylum_final) {
  node <- clade$node
  phylum <- clade$phylum
  edge_nodes <- if (node <= length(tree_phylo$tip.label)) node else c(node, getDescendants(tree_phylo, node))
  branch_df$branch_color[branch_df$node %in% edge_nodes] <- phylum_colors[phylum]
  tip_nodes <- edge_nodes[edge_nodes <= length(tree$tip.label)]
  branch_df$phylum_legend[branch_df$node %in% tip_nodes] <- phylum
}

# -----------------------------
# Define the the septin groups
# -----------------------------
# Root by priority
if ("Sacce1-Myo2" %in% tree$tip.label) {
  highlight_nodes <- data.frame(
    node = c(1083,1238,927,775,1350,1421,1432,1442,768,1256,1301),
    type = "node")
} else if ("Dicdi-GtpA" %in% tree$tip.label) {
  highlight_nodes <- data.frame(
    node = c(1250,1405,1094,943,830,901,912,922,763,1421,1466),
    type = "node")
} else {
  highlight_nodes <- data.frame(
    node = c(1),
    type = "node")
}

# -----------------------------
# Final plot
# -----------------------------
# Add node support values (from tree$node.label)
support_values <- tree$node.label
branch_df$support <- NA
internal_nodes <- (length(tree$tip.label) + 1):max(branch_df$node)
branch_df$support[match(internal_nodes, branch_df$node)] <- support_values

p <- ggtree(tree) %<+% branch_df +
  geom_tree(aes(color = I(branch_color))) +
  geom_tippoint(aes(color = phylum_legend), size = 0, show.legend = TRUE) +  # force legend
  scale_color_manual(name = "Phylum", values = phylum_palette, na.translate = FALSE) +
  geom_tiplab(size = 1.5, hjust = -0.1) +
  geom_nodelab(aes(label = support), size = 1.5, nudge_x = 0.01, nudge_y = 0.5) +
  geom_highlight(data = highlight_nodes,aes(node=node, fill=type),
                 type = "roundrect") +
  theme(legend.position = "right")

for (cl in filtered_class) {
  p <- p + geom_cladelab(node = cl$node, label = cl$label, offset = 0.5)
}

print(p)

ggsave(output_tree, plot = p, width = 20, height = 50, limitsize = FALSE)
