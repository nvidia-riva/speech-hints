# speech-hints-grammars
This project contains grammars for use with Speech hints. 
It currently has support for English alone.

## Getting started
### Exporting the Speech Hints grammar (`far`) file
```bash
python export_to_far.py
```

### Building the ASR Server with speech hints support

```bash
riva-build speech_recognition \
                        <rmir_filename>:<key> <riva_filename>:<key> \
                        --name=conformer-en-US-asr-streaming \
                        --featurizer.use_utterance_norm_params=False \
                        --featurizer.precalc_norm_time_steps=0 \
                        --featurizer.precalc_norm_params=False \
                        --ms_per_timestep=40 \
                        --endpointing.start_history=200 \
                        --nn.fp16_needs_obey_precision_pass \
                        --endpointing.residue_blanks_at_start=-2 \
                        --chunk_size=0.16 \
                        --left_padding_size=1.92 \
                        --right_padding_size=1.92 \
                        --decoder_type=flashlight \
                        --flashlight_decoder.asr_model_delay=-1 \
                        --decoding_language_model_binary=<lm_binary> \
                        --decoding_vocab=<decoder_vocab_file> \
                        --flashlight_decoder.lm_weight=0.8 \
                        --flashlight_decoder.word_insertion_score=1.0 \
                        --flashlight_decoder.beam_size=32 \
                        --flashlight_decoder.beam_threshold=20. \
                        --flashlight_decoder.num_tokenization=1 \
                        --wfst_tokenizer_model=<tokenize_and_classify_far_file> \
                        --wfst_verbalizer_model=<verbalize_far_file> \
                        --speech_hints_model=<speech_hints_far_file> \
                        --language_code=en-US
```

### Using speech hints in Python client

```python
import riva.client
uri = "localhost:50051"  # Default value
auth = riva.client.Auth(uri=uri)
asr_service = riva.client.ASRService(auth)
config = riva.client.RecognitionConfig(
    encoding=riva.client.AudioEncoding.LINEAR_PCM,
    max_alternatives=1,
    profanity_filter=False,
    enable_automatic_punctuation=True,
    verbatim_transcripts=False,
)
my_wav_file=<PATH_TO_YOUR_WAV_FILE>
speech_hints = ["$OOV_ALPHA_SEQUENCE", "i worked at  $OOV_ALPHA_SEQUENCE"]
boost_lm_score = 4.0
riva.client.add_audio_file_specs_to_config(config, my_wav_file)
riva.client.add_word_boosting_to_config(config, speech_hints, boost_lm_score)
```

### Supported ITN Classes
The following classes and phrases are supported:
- $OOV_NUMERIC_SEQUENCE
- $OOV_ALPHA_SEQUENCE
- $OOV_ALPHA_NUMERIC_SEQUENCE
- $ADDRESSNUM
- $FULLPHONENUM
- $POSTALCODE
- $OOV_CLASS_ORDINAL
- $MONTH
- $PERCENT
- $TIME
- $MONEY

# Speech Hints Customization
- Refer to `Tutorial-Customization` Jupyter Notebook