```mermaid
graph TD
    spine1 --> s1 : e1-1
    spine1 --> s2 : e1-2
    spine1 --> s3 : e1-3
    leaf1 --> s1 : e1-49
    leaf1 --> l1 : e1-1
    leaf2 --> s2 : e1-49
    leaf2 --> l2 : e1-1
    leaf3 --> s3 : e1-49
    leaf3 --> l3 : e1-1
    leaf3 --> l4 : e1-2
    leaf3 --> l5 : e1-3
    ce1 --> l1 : eth1
    ce1 --> l2 : eth2
    ce2 --> l3 : eth1
    ce2 --> l4 : eth2
    ce2 --> l5 : eth3
```
