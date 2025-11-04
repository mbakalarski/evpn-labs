```mermaid
graph LR
    %% Auto-generated network topology diagram

    subgraph Spine_Leaf_Networks
        subgraph s1
            spine1 --> s1
            leaf1 --> s1
        end
        subgraph s2
            spine1 --> s2
            leaf2 --> s2
        end
        subgraph s3
            spine1 --> s3
            leaf3 --> s3
        end
    end

    subgraph Leaf_CE_Networks
        subgraph l1
            leaf1 --> l1
            ce1 --> l1
        end
        subgraph l2
            leaf2 --> l2
            ce1 --> l2
        end
        subgraph l3
            leaf3 --> l3
            ce2 --> l3
        end
        subgraph l4
            leaf3 --> l4
            ce2 --> l4
        end
        subgraph l5
            leaf3 --> l5
            ce2 --> l5
        end
    end
```
