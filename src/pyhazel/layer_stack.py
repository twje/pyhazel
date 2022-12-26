from .layer import Layer


class LayerStack:
    def __init__(self) -> None:
        self.layers: list[Layer] = []
        self.layer_index = 0

    def __iter__(self):
        return iter(self.layers)

    def __reversed__(self):
        return self.layers[::-1]

    def push_layer(self, layer: Layer):
        self.layers.insert(self.layer_index, layer)
        self.layer_index += 1
        layer.on_attach()

    def push_overlay(self, overlay: Layer):
        self.layers.append(overlay)
        overlay.on_attach()

    def pop_layer(self, layer: Layer):
        try:
            index = self.layers.index(layer)
            if index > self.layer_index:
                raise Exception()
        except:
            return
        else:
            del self.layers[index]
            self.layer_index -= 1
            layer.on_detach()

    def pop_overlay(self, overlay: Layer):
        try:
            index = self.layers.index(overlay)
            if index < self.layer_index:
                raise Exception()
        except:
            return
        else:
            del self.layers[index]
            overlay.on_detach()

    def destroy(self):
        for layer in self.layers:
            layer.on_detach()
            layer.destroy()
