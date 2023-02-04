import torch
import torch.onnx
#from path import Path
import os

from config import get_opts, get_training_size

from SC_Depth import SC_Depth
from SC_DepthV2 import SC_DepthV2
from SC_DepthV3 import SC_DepthV3


@torch.no_grad()
def main():
    hparams = get_opts()

    if hparams.model_version == 'v1':
        system = SC_Depth(hparams)
    elif hparams.model_version == 'v2':
        system = SC_DepthV2(hparams)
    elif hparams.model_version == 'v3':
        system = SC_DepthV3(hparams)

    system = system.load_from_checkpoint(hparams.ckpt_path, strict=False)

    model = system.depth_net
    model.eval()

    # training size
    training_size = get_training_size(hparams.dataset_name)
    dummy_input = torch.randn(1, 3, *training_size)

    # export the model
    torch.onnx.export(model,
        dummy_input,
        "sc_depth.onnx",
        export_params=True,
        #opset_version=10,
        do_constant_folding=True,
        #input_names=[],
        #output_names=[],
        #dynamic_axes={}
        )

#    output_dir = Path(hparams.output_dir) / \
#        'model_{}'.format(hparams.model_version)
#    output_dir.makedirs_p()


if __name__ == '__main__':
    main()
