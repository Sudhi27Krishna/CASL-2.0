import torch
import numpy as np
from transformer import Transformer

max_sequence_length = 76

input_vocab = ['<START>', ' ', '!', "'", ',', '0', '1', '2', '3', '4', '5', '7', '8', '9', '?', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '<PADDING>', '<END>']
target_vocab = ['<START>', ' ', '!', "'", ',', '0', '1', '2', '3', '4', '5', '7', '8', '9', '?', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '<PADDING>', '<END>']

START_TOKEN = '<START>'
PADDING_TOKEN = '<PADDING>'
END_TOKEN = '<END>'

index_to_target = {k:v for k,v in enumerate(target_vocab)}
target_to_index = {v:k for k,v in enumerate(target_vocab)}
index_to_input = {k:v for k,v in enumerate(input_vocab)}
input_to_index = {v:k for k,v in enumerate(input_vocab)}

d_model = 512
batch_size = 20
ffn_hidden = 1024
num_heads = 8
drop_prob = 0.1
num_layers = 2
max_sequence_length = 76
target_vocab_size = len(target_vocab)

transformer1 = Transformer(d_model, 
                          ffn_hidden,
                          num_heads, 
                          drop_prob, 
                          num_layers, 
                          max_sequence_length,
                          target_vocab_size,
                          input_to_index,
                          target_to_index,
                          START_TOKEN, 
                          END_TOKEN, 
                          PADDING_TOKEN)
     
transformer1.load_state_dict(torch.load("transformer.pth",map_location=torch.device('cpu')))

transformer1.eval()

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

NEG_INFTY = -1e9

def create_masks(inp_batch, tg_batch):
    num_sentences = len(inp_batch)
    look_ahead_mask = torch.full([max_sequence_length, max_sequence_length] , True)
    look_ahead_mask = torch.triu(look_ahead_mask, diagonal=1)
    encoder_padding_mask = torch.full([num_sentences, max_sequence_length, max_sequence_length] , False)
    decoder_padding_mask_self_attention = torch.full([num_sentences, max_sequence_length, max_sequence_length] , False)
    decoder_padding_mask_cross_attention = torch.full([num_sentences, max_sequence_length, max_sequence_length] , False)

    for idx in range(num_sentences):
      inp_sentence_length, tg_sentence_length = len(inp_batch[idx]), len(tg_batch[idx])
      inp_chars_to_padding_mask = np.arange(inp_sentence_length + 1, max_sequence_length)
      tg_chars_to_padding_mask = np.arange(tg_sentence_length + 1, max_sequence_length)
      encoder_padding_mask[idx, :, inp_chars_to_padding_mask] = True
      encoder_padding_mask[idx, inp_chars_to_padding_mask, :] = True
      decoder_padding_mask_self_attention[idx, :, tg_chars_to_padding_mask] = True
      decoder_padding_mask_self_attention[idx, tg_chars_to_padding_mask, :] = True
      decoder_padding_mask_cross_attention[idx, :, inp_chars_to_padding_mask] = True
      decoder_padding_mask_cross_attention[idx, tg_chars_to_padding_mask, :] = True

    encoder_self_attention_mask = torch.where(encoder_padding_mask, NEG_INFTY, 0)
    decoder_self_attention_mask =  torch.where(look_ahead_mask + decoder_padding_mask_self_attention, NEG_INFTY, 0)
    decoder_cross_attention_mask = torch.where(decoder_padding_mask_cross_attention, NEG_INFTY, 0)
    return encoder_self_attention_mask, decoder_self_attention_mask, decoder_cross_attention_mask


def translate(input_sentence): #translate function
  input_sentence = (input_sentence,)
  target_sentence = ("",)
  for word_counter in range(max_sequence_length):
    encoder_self_attention_mask, decoder_self_attention_mask, decoder_cross_attention_mask= create_masks(input_sentence, target_sentence)
    predictions = transformer1(input_sentence,
                              target_sentence,
                              encoder_self_attention_mask, 
                              decoder_self_attention_mask, 
                              decoder_cross_attention_mask,
                              enc_start_token=False,
                              enc_end_token=False,
                              dec_start_token=True,
                              dec_end_token=False)
    next_token_prob_distribution = predictions[0][word_counter]
    next_token_index = torch.argmax(next_token_prob_distribution).item()
    next_token = index_to_target[next_token_index]
    target_sentence = (target_sentence[0] + next_token, )
    if next_token == END_TOKEN:
      break
  return target_sentence[0]
