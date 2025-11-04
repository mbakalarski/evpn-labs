```mermaid
graph TD
    %% Auto-generated network topology
    subgraph Spine_Leaf_Networks
        subgraph s1
            spine1 --> s1 : e1-1
            leaf1 --> s1 : e1-49
        end
        subgraph s2
            spine1 --> s2 : e1-2
            leaf2 --> s2 : e1-49
        end
        subgraph s3
            spine1 --> s3 : e1-3
            leaf3 --> s3 : e1-49
        end
    end
    subgraph Leaf_CE_Networks
        subgraph l1
            leaf1 --> l1 : e1-1
            ce1 --> l1 : eth1
        end
        subgraph l2
            leaf2 --> l2 : e1-1
            ce1 --> l2 : eth2
        end
        subgraph l3
            leaf3 --> l3 : e1-1
            ce2 --> l3 : eth1
        end
        subgraph l4
            leaf3 --> l4 : e1-2
            ce2 --> l4 : eth2
        end
        subgraph l5
            leaf3 --> l5 : e1-3
            ce2 --> l5 : eth3
        end
    end
```
