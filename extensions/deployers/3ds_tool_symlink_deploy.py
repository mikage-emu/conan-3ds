import os

def deploy(graph, output_folder):
    """
    Create a symlink to host package binaries in the current directory
    """
    conanfile = graph.root.conanfile
    for dep in conanfile.dependencies.filter({"direct": True, "build": True}).values():
        pkg_output_folder = os.path.join(output_folder, dep.ref.name)
        bin_folder = os.path.join(dep.package_folder, 'bin')
        try:
            if os.path.islink(pkg_output_folder):
                os.remove(pkg_output_folder)
            os.symlink(bin_folder, pkg_output_folder)
            conanfile.output.info("Creating symlink %s -> %s" % (dep.ref.name, bin_folder))
        except Exception as e:
            conanfile.output.warning("Skipping symlink for %s: %s" % (dep.ref.name, e))
